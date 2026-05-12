import { useEffect, useState } from "react";

function Dashboard() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/api/v1/auth/me", {
          credentials: "include",
        });
        const data = await res.json();

        if (data.status === "SUCCESS") {
          setUser(data.data);
        } else {
          console.error("Failed to fetch user details:", data.message);
        }
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    };
    fetchUser();
  }, []);

  const handleLogout = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/v1/auth/logout", {
        method: "GET",
        credentials: "include",
      });
      const data = await res.json();

      if (data.status === "SUCCESS") {
        setUser(null);
        window.location.href = "/";
      } else {
        console.error("Failed to logout:", data.message);
      }
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <>
      <section id="center">
        <div className="hero">
          <img
            src={user?.picture}
            className="base"
            width="170"
            height="179"
            alt="User Image Not Available"
          />
        </div>
        <div>
          <h1>Dashboard</h1>
          <p>
            Welcome {user && user?.new === true ? "Back" : "New User"},{" "}
            {user ? user.name.split(" ")[0] : "User"}! <br />
            This is your dashboard where you can view your profile information
            and manage your account settings.
          </p>
          <br />
          <p>
            <strong>Name:</strong>{" "}
            {user ? user.name : "User Name Not Available"} <br />
            <strong>Email:</strong>{" "}
            {user ? user.email : "User Email Not Available"}
          </p>
        </div>
        <button
          type="button"
          className="counter"
          onClick={() => handleLogout()}
        >
          Sign Out
        </button>
      </section>
    </>
  );
}

export default Dashboard;
