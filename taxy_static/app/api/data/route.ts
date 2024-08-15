// app/api/data/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  // Fetch data from an external API or perform server-side logic
  const response = await fetch('http://127.0.0.1:5000/api/data');
  const data = await response.json();

  return NextResponse.json(data);
}
