import React, { useState, useEffect } from "react";
import axios from "axios";

export const backendServerUrl = "http://127.0.0.1:5000";

const ProjectSelection = () => {
  const [allProjects, setAllProjects] = useState([]);
  const [newProjectName, setNewProjectName] = useState("");
  const [newProjectId, setNewProjectId] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");
  const [manualProjectId, setManualProjectId] = useState("");

  const userId = localStorage.getItem("userId");

  const fetchAllProjects = async () => {
    try {
      const response = await axios.get(backendServerUrl + "/get_all_projects");
      setAllProjects(response.data.projects || []);
    } catch (error) {
      console.error("Error fetching all projects:", error);
    }
  };

  const joinProject = async (projectId) => {
    if (!projectId) {
      alert("Please enter a valid project ID.");
      return;
    }
    try {
      await axios.post(backendServerUrl + "/join_project", null, {
        params: { userId, projectId },
      });
      alert("Joined project successfully!");
      setManualProjectId("");
      fetchAllProjects();
    } catch (error) {
      alert("Failed to join project.");
    }
  };

  const leaveProject = async (projectId) => {
    try {
      await axios.post(backendServerUrl + "/leave_project", null, {
        params: { userId, projectId },
      });
      alert("Left project successfully!");
      fetchAllProjects();
    } catch (error) {
      alert("Failed to leave project.");
    }
  };

  const createProject = async () => {
    if (!userId) {
      alert("User not logged in.");
      return;
    }
  
    try {
      const response = await axios.post(backendServerUrl + "/create_project", null, {
        params: {
          userId,
          projectId: newProjectId,
          projectName: newProjectName,
          description: newProjectDesc,
        },
      });
      alert("Project created successfully!");
      fetchAllProjects();
    } catch (error) {
      if (error.response && error.response.data?.log === "project already exists") {
        alert(`Project ID "${newProjectId}" already exists. Please choose a different one.`);
      } else {
        alert("Failed to create project.");
      }
      console.error("Error creating project:", error);
    }
  };
  
  const logOut = () => {
    localStorage.removeItem("userId");
    setAllProjects([]);
    alert("Logged out successfully!");
    window.location.reload();
  };

  useEffect(() => {
    if (userId) {
      fetchAllProjects();
    }
  }, [userId]);

  const joinedProjects = allProjects.filter(p => p.users?.includes(userId));
  const notJoinedProjects = allProjects.filter(p => !p.users?.includes(userId));

  const renderProjectList = (projects, actionLabel, actionFn, actionColor) => (
    <ul style={{ listStyleType: "none", padding: 0 }}>
      {projects.map((project, index) => (
        <li key={index} style={{
          border: "1px solid #ccc",
          borderRadius: "12px",
          padding: "16px",
          marginBottom: "12px",
          background: "#f9f9f9",
          boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
        }}>
          <h4>{project.projectName}</h4>
          <p style={{ fontStyle: "italic", color: "#555" }}>
            {project.description || "No description provided."}
          </p>
          <button
            onClick={() => actionFn(project.projectId)}
            style={{
              backgroundColor: actionColor,
              color: "#fff",
              border: "none",
              padding: "8px 12px",
              borderRadius: "6px"
            }}
          >
            {actionLabel}
          </button>
        </li>
      ))}
    </ul>
  );

  return (
    <div style={{ padding: "20px", maxWidth: "700px", margin: "auto" }}>
      <h2>Project Selection</h2>

      <h3>Create a New Project</h3>
      <input type="text" value={newProjectName} onChange={e => setNewProjectName(e.target.value)} placeholder="Project Name" />
      <input type="text" value={newProjectId} onChange={e => setNewProjectId(e.target.value)} placeholder="Project ID" />
      <input type="text" value={newProjectDesc} onChange={e => setNewProjectDesc(e.target.value)} placeholder="Description" />
      <button onClick={createProject} style={{ marginBottom: "20px" }}>Create Project</button>

      <h3>Your Projects</h3>
      {joinedProjects.length > 0 ? renderProjectList(joinedProjects, "Leave", leaveProject, "#e74c3c") : <p>No projects joined yet.</p>}

      <h3>Other Available Projects</h3>
      {notJoinedProjects.length > 0 ? renderProjectList(notJoinedProjects, "Join", joinProject, "#2ecc71") : <p>No other projects found.</p>}

      <h3>Join a Project by ID</h3>
      <input
        type="text"
        placeholder="Enter Project ID"
        value={manualProjectId}
        onChange={(e) => setManualProjectId(e.target.value)}
        style={{ padding: "8px", marginRight: "8px", width: "70%" }}
      />
      <button
        onClick={() => joinProject(manualProjectId)}
        style={{ backgroundColor: "#3498db", color: "#fff", border: "none", padding: "8px 12px", borderRadius: "6px" }}
      >
        Join Project
      </button>

      <div style={{ marginTop: "30px" }}>
        <button onClick={logOut}>Log Out</button>
      </div>
    </div>
  );
};

export default ProjectSelection;
