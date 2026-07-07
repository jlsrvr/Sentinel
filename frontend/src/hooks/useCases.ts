import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchCases, fetchCase, fetchDecisions, assignCase, startReview, submitDecision } from '../api/cases';
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

export function useAssignCase(caseId: string) {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: () => assignCase(caseId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['case', caseId] });
        },
    });
}

export function useStartReview(caseId: string) {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: () => startReview(caseId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['case', caseId] });
        },
    });
}

export function useSubmitDecision(caseId: string) {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (body: Parameters<typeof submitDecision>[1]) => submitDecision(caseId, body),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['case', caseId] });
            queryClient.invalidateQueries({ queryKey: ['decisions', caseId] });
        },
    });
}