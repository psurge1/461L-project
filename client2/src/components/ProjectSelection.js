import React, { useState, useEffect } from "react";
import axios from "axios";

export const backendServerUrl = "http://localhost:5000"

const ProjectSelection = () => {
  const [projects, setProjects] = useState([]); // Stores user projects
  const [newProjectName, setNewProjectName] = useState(""); // Input for new project
  const [newProjectId, setNewProjectId] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");
  const [userId, setUserId] = useState(""); // Input for user ID
  

  // Function to fetch user's project list
  const fetchProjects = async () => {
    try {
      const response = await axios.get(backendServerUrl + "/get_user_projects_list", {
        params: { userId },
      });
      setProjects(response.data.projects);
    } catch (error) {
      console.error("Error fetching projects:", error);
    }
  };

  // Function to join a project
  const joinProject = async (projectId) => {
    try {
      await axios.post(backendServerUrl + "/join_project", { userId, projectId });
      alert("Joined project successfully!");
      fetchProjects(); // Refresh project list
    } catch (error) {
      console.error("Error joining project:", error);
    }
  };

  // Function to create a new project
  const createProject = async () => {
    try {
      await axios.post(backendServerUrl + "/create_project", {
        name: newProjectName,
        id: newProjectId,
        description: newProjectDesc,
      });
      alert("Project created successfully!");
      fetchProjects(); // Refresh project list
    } catch (error) {
      console.error("Error creating project:", error);
    }
  };
  

  //TODO log out function
  //check inside functions of this
  const logOut = async () => {
    setUserId(""); // Clear user ID to log the user out
    setProjects([]); // Optionally clear projects as well
    alert("Logged out successfully!");
  };
  

  return (
<div style={{ padding: "20px" }}>
      <h2>Project Selection</h2>

      {/* Create a New Project */}
      <h3>Create a New Project</h3>
      <input
        type="text"
        value={newProjectName}
        onChange={(e) => setNewProjectName(e.target.value)}
        placeholder="Project Name"
      />
      <input
        type="text"
        value={newProjectId}
        onChange={(e) => setNewProjectId(e.target.value)}
        placeholder="Project ID"
      />
      <input
        type="text"
        value={newProjectDesc}
        onChange={(e) => setNewProjectDesc(e.target.value)}
        placeholder="Project Description"
      />
      <button onClick={createProject}>Create Project</button>


    
      {/* Join an Existing Project */}
      {/* Project ID Input */}
      <h3>Your Projects</h3>
    
      {projects.length === 0 ? (
        <p>No projects found. Join or create one!</p>
      ) : (
        <ul>
          {projects.map((project) => (
            <li key={project.id}>
              {project.name} - {project.description}
              <button onClick={() => joinProject(project.id)}>Join</button>
            </li>
          ))}
        </ul>
      )}
      <h3>Join Existing Projects</h3>
      <div>
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        placeholder="Enter the project ID"
        />
      <button onClick={fetchProjects}>Join My Projects</button>
      
    </div>
      {/* Log Out Button */}
      <div style={{ marginTop: "20px" }}>
        <button onClick={logOut}>Log Out</button>
      </div>
    </div>
  );
};

export default ProjectSelection;
