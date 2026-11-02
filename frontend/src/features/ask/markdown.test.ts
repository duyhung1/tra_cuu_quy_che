import { describe, expect, it } from 'vitest';
import { renderMarkdown } from './markdown';

describe('renderMarkdown', () => {
  it('render danh sách và in đậm', () => {
    const html = renderMarkdown('**3 đợt**:\n\n- 30% tạm ứng\n- 50% sau nghiệm thu');
    expect(html).toContain('<strong>3 đợt</strong>');
    expect(html).toContain('<li>30% tạm ứng</li>');
  });

  it('loại bỏ <img onerror> và <script>', () => {
    const html = renderMarkdown('Xin chào <img src=x onerror="alert(1)"> <script>alert(2)</script>');
    expect(html).not.toContain('onerror');
    expect(html).not.toContain('<script');
  });

  it('chặn link javascript:', () => {
    const html = renderMarkdown('[bấm](javascript:alert(1))');
    expect(html).not.toContain('javascript:');
  });
});
