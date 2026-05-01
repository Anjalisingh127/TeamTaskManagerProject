import { useEffect, useState } from 'react';
import API from '../api/axios';

const TaskList = () => {
    const [tasks, setTasks] = useState([]);

    const fetchTasks = async () => {
        try {
            // In a real app, you'd filter by project, 
            // for now let's show all tasks from the dashboard logic
            const res = await API.get('/dashboard/summary'); 
            // Note: You'll want to add a GET /tasks route in main.py 
            // if you want a full list!
        } catch (err) { console.error(err); }
    };

    const updateStatus = async (id, newStatus) => {
        await API.patch(`/tasks/${id}`, { status: newStatus });
        fetchTasks();
    };

    return (
        <div className="p-8">
            <h2 className="text-xl font-bold mb-4">My Tasks</h2>
            {/* Map through tasks here once the GET /tasks endpoint is called */}
            <p className="text-gray-500 italic">Task tracking ready for live data.</p>
        </div>
    );
};

export default TaskList;