<script lang="ts">
    import { onMount } from 'svelte';
  
    type Crypto = {
      name: string;
      symbol: string;
      current_price: number;
      market_cap: number;
      total_volume: number;
      image: string;
    };
  
    let data: Crypto[] = [];
    let error: string | null = null;
  
    // Fetch los datos al montar el componente
    onMount(async () => {
      try {
        const response = await fetch('http://localhost:5000/api/criptomonedas');
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const json = await response.json();
        if (json.success) {
          data = json.data;
        } else {
          throw new Error('La respuesta no es exitosa');
        }
      } catch (err:any) {
        error = err.message || 'Error desconocido';
      }
    });
  </script>
  
  <style>
    h1{
        font-size: 20px;
        font-weight: bold;
    }
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
      background-color: #f5f5f5;
    }
  
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
  
    th,
    td {
      border: 1px solid #ddd;
      padding: 10px;
      text-align: center;
    }
  
    th {
      background-color: #4CAF50;
      color: white;
    }
  
    tr:nth-child(even) {
      background-color: #f2f2f2;
    }
  
    tr:hover {
      background-color: #ddd;
    }
  
    .container {
      max-width: 800px;
      margin: auto;
      padding: 20px 10px 10px 10px;
    }
  
    h1 {
      text-align: center;
    }
  
    .error {
      color: red;
      text-align: center;
      margin: 20px 0;
    }

    img{
        width: 50px;
        height: 50px;
        margin: auto;
    }
  </style>
  
  <div class="container">
    <h1>Cryptocurrency Information</h1>
    {#if error}
      <p class="error">{error}</p>
    {:else if data.length > 0}
      <table>
        <thead>
          <tr>
            <th>Currency</th>
            <th>Name</th>
            <th>Symbol</th>
            <th>Price</th>
            <th>Market Cap</th>
            <th>Volume (24h)</th>
          </tr>
        </thead>
        <tbody>
          {#each data as cripto}
            <tr>
              <td> <img src={cripto.image} alt="currency"/> </td>
              <td>{cripto.name}</td>
              <td>{cripto.symbol.toUpperCase()}</td>
              <td>${cripto.current_price}</td>
              <td>${cripto.market_cap.toLocaleString()}</td>
              <td>${cripto.total_volume.toLocaleString()}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {:else}
      <p>Loading data...</p>
    {/if}
  </div>
  