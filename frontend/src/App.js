import { useEffect, useState } from "react";
import { request } from "graphql-request";

const API_URL = "http://0.0.0.0:8000/graphql";

const GET_USERS = `
  query {
    getUsers {
      id
      name
      email
    }
  }
`;

function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers()
  }, []);

  const fetchUsers = () => {
    request(API_URL, GET_USERS)
      .then((data) => setUsers(data.getUsers))
      .catch((error) => console.error(error));
  }

  const addUser = (event) => {
    event.preventDefault();
    const form = event.target;
    const name = form.name.value;
    const email = form.email.value;

    const ADD_USER = `
      mutation {
        createUser(name: "${name}", email: "${email}") {
          id
          name
          email
        }
      }
    `;

    request(API_URL, ADD_USER)
      .then((data) => fetchUsers())
      .catch((error) => console.error(error));
  }

  return (
    <div>
      <h1>User list</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name} - {user.email}</li>
        ))}
      </ul>

      <form onSubmit={addUser}>
        <input name="name" placeholder="name"/>
        <input name="email" placeholder="email"/>
        <input type="submit"/>
      </form>
    </div>
  );
}

export default App;