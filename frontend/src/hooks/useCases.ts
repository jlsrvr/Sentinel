import { useQuery } from '@tanstack/react-query';
import { fetchCases, fetchCase, fetchDecisions } from '../api/cases';
import type { Case } from '../types/case';
import type { Decision } from '../types/decision';

export function useCases(skip: number = 0, limit: number = 20) {
    return useQuery<Case[]>({
        queryKey: ['cases', skip, limit],
        queryFn: () => fetchCases(skip, limit),
    });
}

export function useCase(id: string) {
    return useQuery<Case>({
        queryKey: ['case', id],
        queryFn: () => fetchCase(id),
    });
}

export function useDecisions(caseId: string) {
    return useQuery<Decision[]>({
        queryKey: ['decisions', caseId],
        queryFn: () => fetchDecisions(caseId),
    });
}