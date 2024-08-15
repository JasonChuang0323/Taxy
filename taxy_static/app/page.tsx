// app/page.tsx
import React from 'react';

async function fetchData() {
  const response = await fetch('http://127.0.0.1:5000/api/list_user', {
    cache: 'no-store', // This ensures fresh data on every request
  });
  if (!response.ok) {
    throw new Error('Failed to fetch data');
  }
  return response.json();
}

export default async function HomePage() {
  const data = await fetchData();

  return (
    <div>
      <h1>Hello, ll</h1>
      <pre>{JSON.stringify(data)}</pre>
    </div>
  );
}
