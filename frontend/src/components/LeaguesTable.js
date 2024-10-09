import React, { useEffect, useState } from "react";

const LeaguesTable = () => {
  const [leagues, setLeagues] = useState([]);
  const [error, setError] = useState(null);
  const token = sessionStorage.getItem("token"); // Get the token from sessionStorage

  useEffect(() => {
    const fetchLeagues = async () => {
      try {
        const response = await fetch("http://localhost:8000/leagues/", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`, // Include the token in the Authorization header
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch leagues");
        }

        const data = await response.json();
        console.log(data); 


        setLeagues(data.slice(0, 10)); // Assuming the API returns an array of leagues
      } catch (err) {
        setError(err.message);
      }
    };

    fetchLeagues();
  }, [token]);

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>; // Display error message if there's an error
  }

  return (
    <div>
      <h2>Leagues</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Level</th>
          </tr>
        </thead>
        <tbody>
          {leagues.map((league) => (
            <tr key={league.id}>
              <td>{league.id}</td>
              <td>{league.league_name}</td>
              <td>{league.level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LeaguesTable;
