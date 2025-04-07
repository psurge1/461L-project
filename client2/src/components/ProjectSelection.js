import React, { useState, useEffect } from "react";
import axios from "axios";

export const backendServerUrl = "http://127.0.0.1:5000";

const ProjectSelection = () => {
  const [projects, setProjects] = useState([]);
  const [newProjectName, setNewProjectName] = useState("");
  const [newProjectId, setNewProjectId] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");
  const [manualProjectId, setManualProjectId] = useState("");

  const userId = localStorage.getItem("userId");

  const fetchProjects = async () => {
    try {
      const response = await axios.get(backendServerUrl + "/get_user_projects_list", {
        params: { userId },
      });
      console.log("Fetched projects response:", response.data);
      setProjects(response.data.projects || []);
    } catch (error) {
      console.error("Error fetching projects:", error);
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
      setManualProjectId(""); // clear input
      fetchProjects();
    } catch (error) {
      console.error("Error joining project:", error);
      alert("Failed to join project. Make sure the ID is correct.");
    }
  };

  const leaveProject = async (projectId) => {
    try {
      await axios.post(backendServerUrl + "/leave_project", null, {
        params: { userId, projectId },
      });
      alert("Left project successfully!");
      fetchProjects();
    } catch (error) {
      console.error("Error leaving project:", error);
    }
  };

  const createProject = async () => {
    if (!userId) {
      alert("User not logged in.");
      return;
    }

    try {
      await axios.post(backendServerUrl + "/create_project", null, {
        params: {
          userId,
          projectId: newProjectId,
          projectName: newProjectName,
          description: newProjectDesc,
        },
      });
      alert("Project created successfully!");
      fetchProjects();
    } catch (error) {
      console.error("Error creating project:", error);
    }
  };

  const logOut = () => {
    localStorage.removeItem("userId");
    setProjects([]);
    alert("Logged out successfully!");
    window.location.reload();
  };

  useEffect(() => {
    if (userId) {
      fetchProjects();
    }
  }, [userId]);

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
      <h2>Project Selection</h2>

      <h3>Create a New Project</h3>
      <input
        type="text"
        value={newProjectName}
        onChange={(e) => setNewProjectName(e.target.value)}
        placeholder="Project Name"
        style={{ padding: "8px", width: "100%", marginBottom: "8px" }}
      />
      <input
        type="text"
        value={newProjectId}
        onChange={(e) => setNewProjectId(e.target.value)}
        placeholder="Project ID"
        style={{ padding: "8px", width: "100%", marginBottom: "8px" }}
      />
      <input
        type="text"
        value={newProjectDesc}
        onChange={(e) => setNewProjectDesc(e.target.value)}
        placeholder="Project Description"
        style={{ padding: "8px", width: "100%", marginBottom: "8px" }}
      />
      <button onClick={createProject} style={{ marginBottom: "24px" }}>
        Create Project
      </button>

      <h3>Your Projects</h3>
      {projects.length === 0 ? (
        <p>No projects found. Join or create one!</p>
      ) : (
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {projects.map((project, index) => {
            const isInProject = project.users && project.users.includes(userId);

            return (
              <li key={index} style={{
                border: "1px solid #ccc",
                borderRadius: "12px",
                padding: "16px",
                marginBottom: "12px",
                background: "#f9f9f9",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
              }}>
                <h4 style={{ margin: "0 0 8px" }}>{project.projectName}</h4>
                <p style={{ margin: "0 0 12px", fontStyle: "italic", color: "#555" }}>
                  {project.description || "No description provided."}
                </p>
                {isInProject ? (
                  <button
                    style={{ backgroundColor: "#e74c3c", color: "#fff", border: "none", padding: "8px 12px", borderRadius: "6px" }}
                    onClick={() => leaveProject(project.projectId)}
                  >
                    Leave
                  </button>
                ) : (
                  <button
                    style={{ backgroundColor: "#2ecc71", color: "#fff", border: "none", padding: "8px 12px", borderRadius: "6px" }}
                    onClick={() => joinProject(project.projectId)}
                  >
                    Join
                  </button>
                )}
              </li>
            );
          })}
        </ul>
      )}

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
