import type { Case } from "../types/case";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

function fetchCases(skip: number = 0, limit: number = 20): Promise<Case[]> {
    return fetch(`${BASE_URL}/api/v1/cases/?skip=${skip}&limit=${limit}`)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to fetch cases");
            }
            return response.json();
        })
        .then((data) => data as Case[]);
}

export { fetchCases };