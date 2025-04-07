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
  const [projectId, setProjectId] = useState("");

  const userId = localStorage.getItem("userId");

  useEffect(() => {
    const fetchAllHardware = async () => {
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
        setLoading(false);
      } catch (error) {
        console.error("Failed to load hardware sets:", error);
        setMessage("Failed to load hardware sets.");
        setLoading(false);
      }
    };

    fetchAllHardware();
  }, []);

  const handleAmountChange = (name, value) => {
    if (value >= 0) {
      setAmounts(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleCheckout = async (setName) => {
    if (!projectId || !userId) {
      alert("Please enter a project ID.");
      return;
    }
    try {
      await axios.post(
        `${backendServerUrl}/check_out`,
        {
          setNumber: setName,
          amount: Number(amounts[setName] || 0),
          projectId,
          userId,
        },
        { headers: { "Content-Type": "application/json" } }
      );
      setMessage(`Checked out ${amounts[setName]} from ${setName}`);
      window.location.reload();
    } catch (error) {
      console.error("Checkout failed:", error);
      setMessage(error.response?.data?.log || "Checkout failed!");
    }
  };

  const handleCheckin = async (setName) => {
    if (!projectId || !userId) {
      alert("Please enter a project ID.");
      return;
    }
    try {
      await axios.post(
        `${backendServerUrl}/check_in`,
        {
          setNumber: setName,
          amount: Number(amounts[setName] || 0),
          projectId,
          userId,
        },
        { headers: { "Content-Type": "application/json" } }
      );
      setMessage(`Checked in ${amounts[setName]} to ${setName}`);
      window.location.reload();
    } catch (error) {
      console.error("Check-in failed:", error);
      setMessage(error.response?.data?.log || "Check-in failed!");
    }
  };

  const handleCreateSet = async () => {
    try {
      await axios.post(`${backendServerUrl}/create_hardware_set`, null, {
        params: {
          hwSetName: newSetName,
          capacity: newSetCapacity,
        },
      });
      setMessage(`Created ${newSetName}`);
      window.location.reload();
    } catch (error) {
      console.error("Creation failed:", error);
      setMessage("Creation failed!");
    }
  };

  const handleDeleteSet = async (setName) => {
    try {
      await axios.delete(`${backendServerUrl}/remove_hardware_set`, {
        params: { hwSetName: setName },
      });
      setMessage(`Deleted ${setName}`);
      window.location.reload();
    } catch (error) {
      console.error("Delete failed:", error);
      setMessage("Delete failed!");
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "40px auto", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2 style={{ textAlign: "center", marginBottom: "30px" }}>🔧 Resource Management</h2>

      {message && <p style={{ color: "green", textAlign: "center" }}>{message}</p>}

      <div style={{ marginBottom: "20px", textAlign: "center" }}>
        <label>
          <strong>Project ID: </strong>
          <input
            type="text"
            placeholder="Enter project ID"
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
            style={{ padding: "8px", marginLeft: "10px", width: "200px" }}
          />
        </label>
      </div>

      {loading ? (
        <p style={{ textAlign: "center" }}>Loading hardware sets...</p>
      ) : (
        <>
          {hardwareSets.map((set) => (
            <div
              key={set.name}
              style={{
                border: "1px solid #ccc",
                borderRadius: "10px",
                padding: "20px",
                marginBottom: "20px",
                boxShadow: "2px 2px 10px rgba(0,0,0,0.1)",
              }}
            >
              <h3>{set.name}</h3>
              <p>
                <strong>Availability:</strong> {set.availability} / <strong>Capacity:</strong> {set.capacity}
              </p>
              <input
                type="number"
                min="0"
                value={amounts[set.name] || ""}
                onChange={(e) => handleAmountChange(set.name, e.target.value)}
                placeholder="Enter amount"
                style={{ padding: "8px", marginRight: "10px", width: "100px" }}
              />
              <button
                onClick={() => handleCheckout(set.name)}
                style={{ padding: "8px 16px", marginRight: "10px" }}
              >
                Check Out
              </button>
              <button
                onClick={() => handleCheckin(set.name)}
                style={{ padding: "8px 16px", marginRight: "10px" }}
              >
                Check In
              </button>
              <button
                onClick={() => handleDeleteSet(set.name)}
                style={{ padding: "8px 16px", backgroundColor: "#ff4d4f", color: "white" }}
              >
                Remove
              </button>
            </div>
          ))}

          <hr style={{ margin: "40px 0" }} />
          <h3>Create New Hardware Set</h3>
          <div style={{ marginBottom: "20px" }}>
            <input
              type="text"
              placeholder="Set Name"
              value={newSetName}
              onChange={(e) => setNewSetName(e.target.value)}
              style={{ padding: "8px", marginRight: "10px" }}
            />
            <input
              type="number"
              min="0"
              placeholder="Capacity"
              value={newSetCapacity}
              onChange={(e) => setNewSetCapacity(e.target.value)}
              style={{ padding: "8px", marginRight: "10px", width: "100px" }}
            />
            <button onClick={handleCreateSet} style={{ padding: "8px 16px" }}>
              Create Set
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default ResourceManagement;
