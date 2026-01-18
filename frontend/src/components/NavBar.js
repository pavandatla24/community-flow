// import { NavLink } from "react-router-dom";

// const linkStyle = ({ isActive }) => ({
//   padding: "8px 12px",
//   borderRadius: 8,
//   textDecoration: "none",
//   color: isActive ? "white" : "#111",
//   background: isActive ? "#111" : "transparent",
// });

// export default function NavBar() {
//   return (
//     <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 18 }}>
//       <NavLink to="/" style={linkStyle}>Home</NavLink>
//       <NavLink to="/themes" style={linkStyle}>Themes</NavLink>
//       <NavLink to="/clusters" style={linkStyle}>Clusters</NavLink>
//       <NavLink to="/map" style={linkStyle}>Map</NavLink>
//       <NavLink to="/report" style={linkStyle}>Report</NavLink>
//     </div>
//   );
// }

// frontend/src/components/NavBar.js

import React from "react";
import { NavLink } from "react-router-dom";

export default function NavBar() {
  return (
    <div style={styles.wrap}>
      <div style={styles.inner}>
        <div style={styles.brand}>Community Flow</div>

        <nav style={styles.nav}>
          <NavItem to="/">Home</NavItem>
          <NavItem to="/clusters">Clusters</NavItem>
          <NavItem to="/map">Map</NavItem>
          <NavItem to="/report">Report</NavItem>
        </nav>
      </div>
    </div>
  );
}

function NavItem({ to, children }) {
  return (
    <NavLink
      to={to}
      end={to === "/"}
      style={({ isActive }) => ({
        ...styles.link,
        ...(isActive ? styles.active : {}),
      })}
    >
      {children}
    </NavLink>
  );
}

const styles = {
  wrap: {
    position: "sticky",
    top: 0,
    zIndex: 10,
    background: "#fff",
    borderBottom: "1px solid #e5e7eb",
  },
  inner: {
    maxWidth: 980,
    margin: "0 auto",
    padding: "12px 14px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif',
  },
  brand: { fontWeight: 800, color: "#111827" },
  nav: { display: "flex", gap: 10 },
  link: {
    textDecoration: "none",
    color: "#374151",
    fontSize: 14,
    padding: "8px 10px",
    borderRadius: 10,
  },
  active: {
    color: "#111827",
    background: "#f3f4f6",
    fontWeight: 700,
  },
};
