import { useQuery } from '@tanstack/react-query';
import { listDocuments, type DocumentsResponse } from '../../shared/api/documents';

export const DOCUMENTS_KEY = ['documents'] as const;

/** Danh sách tài liệu; tự poll 3 s chỉ khi còn tài liệu đang chờ / đang xử lý. */
export function useDocuments() {
  return useQuery<DocumentsResponse>({
    queryKey: DOCUMENTS_KEY,
    queryFn: listDocuments,
    refetchInterval: (query) => ((query.state.data?.counts.processing ?? 0) > 0 ? 3000 : false),
  });
}
