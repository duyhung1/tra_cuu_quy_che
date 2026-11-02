# Hạ tầng AWS — MVP (T-006)

Một môi trường duy nhất, vùng `ap-southeast-1`. Các bước dưới đây làm **thủ công một lần** bằng AWS Console hoặc CLI. Terraform để giai đoạn 2.

> ⚠ **MVP không có đăng nhập.** Security group của ALB phải **chỉ cho phép dải IP / VPN công ty**. Đây là lớp bảo vệ duy nhất cho tài liệu kinh doanh. Không bao giờ mở `0.0.0.0/0`.

## 1. Cần chuẩn bị

| Hạng mục | Người cung cấp |
|---|---|
| Danh sách dải IP / VPN công ty (CIDR) | IT |
| Tên miền + quyền tạo bản ghi DNS | IT |
| Tài khoản AWS, quyền tạo VPC / EC2 / RDS / S3 / ALB / IAM | Quản lý |
| Khóa Anthropic API | Quản lý |

## 2. Tài nguyên

| Tài nguyên | Cấu hình |
|---|---|
| VPC | 2 public subnet (ALB) + 2 private subnet (EC2, RDS); NAT Gateway để EC2 gọi `api.anthropic.com` và tải model TEI |
| Security group `sg-alb` | Inbound 443 + 80 **chỉ từ CIDR công ty** |
| Security group `sg-app` | Inbound 80 chỉ từ `sg-alb`; không mở SSH (dùng SSM Session Manager) |
| Security group `sg-db` | Inbound 5432 chỉ từ `sg-app` |
| EC2 | `m7i.2xlarge`, Amazon Linux 2023, EBS gp3 100 GB mã hóa. Cài Docker + Compose plugin, AWS CLI. IAM role: `AmazonSSMManagedInstanceCore`, đọc secret `tcqc/prod`, ECR pull, S3 read/write bucket ứng dụng, CloudWatch Logs |
| RDS | PostgreSQL 16, `db.t4g.medium`, 50 GB gp3, mã hóa KMS, backup 7 ngày, không public, `rds.force_ssl=1`. Extension `vector` có sẵn trên RDS PG16 (migration tự `CREATE EXTENSION`) |
| S3 | Bucket `tcqc-documents-prod`, Block Public Access, SSE-KMS, versioning; bucket policy từ chối request không có `aws:SecureTransport` |
| ALB | Listener 443 (chứng chỉ ACM) → target group EC2:80; 80 → redirect 443; idle timeout 120 s; health check `/healthz` |
| Secrets Manager | `tcqc/prod` dạng JSON (xem §3) |
| ECR | Repository `tcqc-api`, `tcqc-web` |
| GitHub Actions | Role OIDC cho phép push ECR → lưu ARN vào secret `AWS_DEPLOY_ROLE_ARN` của repo |

## 3. Secret `tcqc/prod`

```json
{
  "DATABASE_URL": "postgresql+asyncpg://tcqc:<mật khẩu>@<rds-endpoint>:5432/tcqc?ssl=require",
  "S3_BUCKET": "tcqc-documents-prod",
  "S3_USE_KMS": "true",
  "TEI_URL": "http://tei:80",
  "ANTHROPIC_API_KEY": "<khóa>",
  "LLM_MODEL": "claude-opus-5-5",
  "QA_TOP_N": "12"
}
```

## 4. Deploy

Trên EC2 (qua SSM), trong thư mục chứa `docker-compose.prod.yml`, `deploy.sh`, `rollback.sh`:

```bash
export DOMAIN=tcqc.<công-ty>.vn
./deploy.sh sha-<commit>     # tag do CI build khi merge vào main
./rollback.sh                # quay về tag trước
```

**Quy tắc:** chạy `make eval BASE_URL=https://$DOMAIN` và kiểm tra kết quả trước mỗi lần deploy lên môi trường đang có người dùng pilot; deploy ngoài giờ làm việc.

## 5. Kiểm tra sau khi dựng

- [ ] Từ mạng công ty: `curl https://$DOMAIN/healthz` → `{"status":"ok"}`
- [ ] Từ mạng ngoài (ví dụ 4G điện thoại): **không kết nối được**
- [ ] Log `api` / `worker` xuất hiện trong CloudWatch log group `/tcqc/prod`
- [ ] Upload thử 1 PDF → trạng thái Sẵn sàng; hỏi thử 1 câu → có câu trả lời
- [ ] Đặt hạn mức chi tiêu trong Anthropic Console; bật AWS Budgets cảnh báo chi phí

## 6. Số liệu sử dụng trong pilot

```sql
SELECT date_trunc('week', created_at) AS week,
       count(*) FILTER (WHERE status = 'ok')    AS answered,
       count(*) FILTER (WHERE status = 'error') AS errors,
       percentile_cont(0.9) WITHIN GROUP (ORDER BY latency_ms) AS p90_latency_ms
FROM qa_log GROUP BY 1 ORDER BY 1 DESC;
```

## 7. Gỡ một tài liệu (không có trên giao diện trong MVP)

```sql
DELETE FROM documents WHERE filename = '<tên tệp>' RETURNING storage_key;  -- chunk và job tự xóa theo CASCADE
```

Sau đó xóa object tương ứng: `aws s3 rm s3://tcqc-documents-prod/<storage_key>`.
