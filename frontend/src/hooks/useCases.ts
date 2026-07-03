import { useQuery } from '@tanstack/react-query';
import { fetchCases } from '../api/cases';
import type { Case } from '../types/case';

export function useCases(skip: number = 0, limit: number = 20) {
    return useQuery<Case[]>({
        queryKey: ['cases', skip, limit],
        queryFn: () => fetchCases(skip, limit),
    });
}