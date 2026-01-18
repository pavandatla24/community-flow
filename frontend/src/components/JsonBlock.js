export default function JsonBlock({ data }) {
    return (
      <pre
        style={{
          background: "#f6f8fa",
          padding: 12,
          borderRadius: 8,
          overflowX: "auto",
          fontSize: 13,
          lineHeight: 1.4,
        }}
      >
        {JSON.stringify(data, null, 2)}
      </pre>
    );
  }
  