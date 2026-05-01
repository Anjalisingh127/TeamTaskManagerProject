import { useEffect, useState } from 'react';
import API from '../api/axios';

const ProjectManager = () => {
    const [projects, setProjects] = useState([]);
    const [name, setName] = useState('');
    const [desc, setDesc] = useState('');
    const role = localStorage.getItem('role');

    const fetchProjects = async () => {
        const res = await API.get('/projects');
        setProjects(res.data);
    };

    useEffect(() => { fetchProjects(); }, []);

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await API.post('/projects', { name, description: desc });
            setName(''); setDesc('');
            fetchProjects();
            alert("Project Created!");
        } catch (err) { alert("Error creating project"); }
    };

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-6">Projects</h1>
            
            {role === 'admin' && (
                <form onSubmit={handleCreate} className="mb-10 bg-white p-6 rounded shadow-md">
                    <h2 className="font-semibold mb-4 text-blue-600">Create New Project</h2>
                    <input className="border p-2 mr-2 rounded" placeholder="Project Name" value={name} onChange={e => setName(e.target.value)} required />
                    <input className="border p-2 mr-2 rounded" placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)} />
                    <button className="bg-blue-600 text-white px-4 py-2 rounded">Add Project</button>
                </form>
            )}

            <div className="grid gap-4">
                {projects.map(p => (
                    <div key={p.id} className="bg-white p-4 rounded border shadow-sm">
                        <h3 className="font-bold text-lg">{p.name}</h3>
                        <p className="text-gray-600">{p.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ProjectManager;