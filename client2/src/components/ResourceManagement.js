import React, { useState, useEffect } from "react";
import axios from "axios";

const backendServerUrl = "http://127.0.0.1:5000";

const ResourceManagement = () => {
  const [hardwareSets, setHardwareSets] = useState([]);
  const [amounts, setAmounts] = useState({});
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [newSetName, setNewSetName] = useState("");
  const [newSetCapacity, setNewSetCapacity] = useState("");
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState("");
  const [usageMap, setUsageMap] = useState({});

  const userId = localStorage.getItem("userId");

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const hwNamesRes = await axios.get(`${backendServerUrl}/get_all_hw_names`);
        const hwNames = hwNamesRes.data.hwnames || [];

        const hwInfoRequests = hwNames.map(name =>
          axios.get(`${backendServerUrl}/get_hw_info`, {
            params: { hwSetName: name },
          })
        );

        const hwInfoResponses = await Promise.all(hwInfoRequests);
        const hwData = hwNames.map((name, idx) => ({
          name,
          ...hwInfoResponses[idx].data.hwset,
        }));

        setHardwareSets(hwData);

        const projectRes = await axios.get(`${backendServerUrl}/get_user_projects_list`, {
          params: { userId },
        });

        setProjects(projectRes.data.projects || []);

        const usageRes = await axios.get(`${backendServerUrl}/get_project_info`, {
          params: { projectId: projectRes.data.projects[0]?.projectId },
        });

        setUsageMap(usageRes.data.hardware || {});
        setSelectedProject(projectRes.data.projects[0]?.projectId || "");
        setLoading(false);
      } catch (error) {
        console.error("Failed to load data:", error);
        setMessage("Failed to load data.");
        setLoading(false);
      }
    };

    fetchAllData();
  }, [userId]);

  const handleAmountChange = (name, value) => {
    if (value >= 0) {
      setAmounts(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleCheckout = async (setName) => {
    if (!selectedProject || !userId) return;
    try {
      await axios.post(`${backendServerUrl}/check_out`, {
        setNumber: setName,
        amount: Number(amounts[setName] || 0),
        projectId: selectedProject,
        userId,
      });
      setMessage(`Checked out ${amounts[setName]} from ${setName}`);
      window.location.reload();
    } catch (error) {
      console.error("Checkout failed:", error);
      setMessage(error.response?.data?.log || "Checkout failed!");
    }
  };

  const handleCheckin = async (setName) => {
    const currentUsage = usageMap[setName] || 0;
    if (!selectedProject || !userId || Number(amounts[setName]) > currentUsage) {
      alert(`Cannot check in more than you have checked out. Current usage: ${currentUsage}`);
      return;
    }
    try {
      await axios.post(`${backendServerUrl}/check_in`, {
        setNumber: setName,
        amount: Number(amounts[setName] || 0),
        projectId: selectedProject,
        userId,
      });
      setMessage(`Checked in ${amounts[setName]} to ${setName}`);
      window.location.reload();
    } catch (error) {
      console.error("Check-in failed:", error);
      setMessage(error.response?.data?.log || "Check-in failed!");
    }
  };
  return (
    <div style={{ maxWidth: "800px", margin: "40px auto", padding: "20px" }}>
      <h2 style={{ textAlign: "center", marginBottom: "30px" }}>🔧 Resource Management</h2>

      {message && <p style={{ color: "green", textAlign: "center" }}>{message}</p>}

      <div style={{ marginBottom: "20px", textAlign: "center" }}>
        <label>
          <strong>Select Project: </strong>
          <select
            value={selectedProject}
            onChange={(e) => setSelectedProject(e.target.value)}
            style={{ padding: "8px", marginLeft: "10px" }}
          >
            {projects.map((p) => (
              <option key={p.projectId} value={p.projectId}>
                {p.projectId}
              </option>
            ))}
          </select>
        </label>
      </div>

      {loading ? (
        <p style={{ textAlign: "center" }}>Loading hardware sets...</p>
      ) : (
        <>
          {hardwareSets.map((set) => (
            <div
              key={set.name}
              style={{ border: "1px solid #ccc", borderRadius: "10px", padding: "20px", marginBottom: "20px" }}
            >
              <h3>{set.name}</h3>
              <p>
                <strong>Availability:</strong> {set.availability} / <strong>Capacity:</strong> {set.capacity} <br />
                <strong>Checked out in this project:</strong> {usageMap[set.name] || 0}
              </p>
              <input
                type="number"
                min="0"
                value={amounts[set.name] || ""}
                onChange={(e) => handleAmountChange(set.name, e.target.value)}
                placeholder="Enter amount"
                style={{ padding: "8px", marginRight: "10px", width: "100px" }}
              />
              <button onClick={() => handleCheckout(set.name)} style={{ padding: "8px 16px", marginRight: "10px" }}>
                Check Out
              </button>
              <button onClick={() => handleCheckin(set.name)} style={{ padding: "8px 16px", marginRight: "10px" }}>
                Check In
              </button>
            </div>
          ))}

        </>
      )}
    </div>
  );
};

export default ResourceManagement;
