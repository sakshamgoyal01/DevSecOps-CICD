import { useEffect, useState } from "react";

const API = "http://localhost:5001";

function App() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [people, setPeople] = useState([]);

  const fetchPeople = async () => {
    const res = await fetch(`${API}/people`);
    const data = await res.json();
    setPeople(data);
  };

  const submitForm = async (e) => {
    e.preventDefault();
    await fetch(`${API}/people`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age })
    });
    setName("");
    setAge("");
    fetchPeople();
  };

  useEffect(() => {
    fetchPeople();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Add Person</h2>
      <form onSubmit={submitForm}>
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          placeholder="Age"
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          required
        />
        <button type="submit">Save</button>
      </form>

      <h2>People</h2>
      <ul>
        {people.map(p => (
          <li key={p.id}>{p.name} - {p.age}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
