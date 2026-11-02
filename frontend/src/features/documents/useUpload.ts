import { useMutation, useQueryClient } from '@tanstack/react-query';
import { uploadDocuments, type UploadResponse } from '../../shared/api/documents';
import { DOCUMENTS_KEY } from './useDocuments';

export function useUpload() {
  const qc = useQueryClient();
  return useMutation<UploadResponse, Error, File[]>({
    mutationFn: uploadDocuments,
    onSettled: () => qc.invalidateQueries({ queryKey: DOCUMENTS_KEY }),
  });
}
