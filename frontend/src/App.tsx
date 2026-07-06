import CasesPage from './pages/CasesPage.tsx';
import CaseDetails from './pages/CaseDetailPage.tsx'
import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
    {
        path: "/",
        element: <CasesPage />,
    },
    {
        path: "/cases/:id",
        element: <CaseDetails />,
    },
]);

function App() {
    return (
        <RouterProvider router={router} />
    );
}

export default App;