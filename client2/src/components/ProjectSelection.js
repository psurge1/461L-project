import React, { useState, useEffect } from "react";
import axios from "axios";

export const backendServerUrl = "";

const ProjectSelection = () => {
  const [joinedProjects, setJoinedProjects] = useState([]);
  const [newProjectName, setNewProjectName] = useState("");
  const [newProjectId, setNewProjectId] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");
  const [manualProjectId, setManualProjectId] = useState("");

  const userId = localStorage.getItem("userId");

  const fetchJoinedProjects = async () => {
    try {
      const response = await axios.get(backendServerUrl + "/get_user_projects_list", {
        params: { userId },
      });
      return response.data.projects || [];
    } catch (error) {
      console.error("Error fetching joined projects:", error);
      return [];
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
      
      fetchJoinedProjects().then((joined) => {
        setJoinedProjects(joined);
      });
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
      
      fetchJoinedProjects().then((joined) => {
        setJoinedProjects(joined);
      });
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
      
      fetchJoinedProjects().then((joined) => {
        setJoinedProjects(joined);
      });
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
    alert("Logged out successfully!");
    window.location.reload();
  };

  useEffect(() => {
    if (userId) {
      fetchJoinedProjects().then((joined) => {
        setJoinedProjects(joined);
      });
    }
  }, [userId]);

  const renderProjectList = (projects, actionLabel, actionFn, actionColor) => (
    <ul style={{ listStyleType: "none", padding: 0 }}>
      {projects.map((project, index) => (
        <li key={index} style={{
          border: "1px solid #ccc",
          padding: "16px",
          marginBottom: "12px",
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

      <h3>Your Projects</h3>
      {joinedProjects.length > 0 ? renderProjectList(joinedProjects, "Leave", leaveProject, "#e74c3c") : <p>No projects joined yet.</p>}

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

      <h3>Create a New Project</h3>
      <input type="text" value={newProjectName} onChange={e => setNewProjectName(e.target.value)} placeholder="Project Name" />
      <input type="text" value={newProjectId} onChange={e => setNewProjectId(e.target.value)} placeholder="Project ID" />
      <input type="text" value={newProjectDesc} onChange={e => setNewProjectDesc(e.target.value)} placeholder="Description" />
      <button onClick={createProject} style={{ marginBottom: "20px" }}>Create Project</button>


      {userId && (
        <div style={{ marginTop: "30px" }}>
          <button onClick={logOut}>Log Out</button>
        </div>
      )}
    </div>
  );
};

export default ProjectSelection;
