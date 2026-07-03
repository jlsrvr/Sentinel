import { CaseQueue } from './components/cases/CaseQueue';

function App() {
    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-2xl font-medium text-gray-900 mb-6">Sentinel</h1>
                <CaseQueue />
            </div>
        </div>
    );
}

export default App;