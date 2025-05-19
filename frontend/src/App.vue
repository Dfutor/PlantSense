<template>
  <div style="padding: 20px; font-family: sans-serif">
    <h1>📊 Dashboard de Sensor de Humedad YL-69</h1>

    <h2>Últimas Lecturas</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Sensor</th>
          <th>Valor</th>
          <th>Humedad (%)</th>
          <th>Fecha</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lectura in lecturas" :key="lectura.id">
          <td>{{ lectura.id }}</td>
          <td>{{ lectura.id_sensor }}</td>
          <td>{{ lectura.valor }}</td>
          <td>{{ lectura.porcentaje_humedad.toFixed(2) }}</td>
          <td>{{ new Date(lectura.fecha_registro).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>

    <h2>Gráfica en Tiempo Real</h2>
    <canvas id="grafica"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

const lecturas = ref([])
let chart = null

const cargarDatos = async () => {
  try {
    const res = await axios.get('http://192.168.80.15:3000/select/lecturas')
    lecturas.value = res.data.slice(-20) // Mostrar últimas 20 lecturas

    const labels = lecturas.value.map(l => new Date(l.fecha_registro).toLocaleTimeString())
    const datos = lecturas.value.map(l => parseFloat(l.porcentaje_humedad))

    if (chart) {
      chart.data.labels = labels
      chart.data.datasets[0].data = datos
      chart.update()
    } else {
      const ctx = document.getElementById('grafica')
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Humedad (%)',
            data: datos,
            fill: false,
            borderColor: 'blue',
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true, max: 100 }
          }
        }
      })
    }
  } catch (err) {
    console.error('Error cargando lecturas:', err)
  }
}

onMounted(() => {
  cargarDatos()
  setInterval(cargarDatos, 10000) // Actualizar cada 10s
})
</script>

<style>
table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 40px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
th {
  background-color: #f2f2f2;
}
canvas {
  max-width: 100%;
}
</style>
