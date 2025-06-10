const dayjs = require('dayjs');
const { appendFile } = require('fs').promises;
const nodemailer = require('nodemailer');

require('dotenv').config({
  path: process.env.NODE_ENV?.toUpperCase() === 'PROD' ? './.env.prod' : './.env'
});

console.log('Entorno actual:', process.env.NODE_ENV);
// module.exports = { obtenerNombreImagen };
// Cargar las variables de entorno según el valor de NODE_ENV
  const ENVIRONMENT = process.env.ENVIRONMENT;
  const email_from = process.env.USER_EMAIL_FROM;
  const pass_from = process.env.APP_PASS_EMAIL_FROM;
  const email_to = process.env.USER_EMAIL_TO;
  const path = process.env.PATH_SEARCH_IMG;
  const grupos = process.env.GROUPS.split(',');
  const API_KEY = ENVIRONMENT === 'development' ? process.env.API_KEY_DEV : process.env.API_KEY_PROD;


module.exports = { 
  log, 
  obtenerNombreImagen, 
  enviarCorreo, 
  grupos,
  path
};

async function log(mensaje) {
  const timestamp = dayjs().format('YYYY-MM-DD HH:mm:ss');
  await appendFile('./log.txt', `[${timestamp}] ${mensaje}\n`);
}

function obtenerNombreImagen() {
  const ahora = dayjs();
  const hora = ahora.hour();

  if (hora === 15) {//2
    const ayer = ahora.subtract(1, 'day').format('DD-MM-YYYY');
    return `${ayer}.png`;
  } else if (hora === 1) {//14
    const hoy = ahora.format('DD-MM-YYYY');
    return `130_${hoy}.png`;
  } else if (hora === 12) {//17
    const hoy = ahora.format('DD-MM-YYYY');
    return `430_${hoy}.png`;
  }

  return null;
}

async function enviarCorreo(asunto, mensaje) {
  let transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: email_from,
      pass: pass_from
    }
  });

  await transporter.sendMail({
    from: email_from,
    to: email_to,
    subject: asunto,
    text: mensaje
  });
}

// automatizaciones/
// │
// ├── automatizacion_1/
// │   ├── src/                   # Código fuente de la automatización
// │   ├── tests/                 # Pruebas unitarias o de integración
// │   ├── config/                # Archivos de configuración específicos de esta automatización
// │   ├── README.md              # Descripción y uso de esta automatización
// │   └── requirements.txt       # Dependencias para esta automatización (si aplica)
// │
// ├── automatizacion_2/
// │   ├── src/                   
// │   ├── tests/                 
// │   ├── config/                
// │   ├── README.md
// │   └── requirements.txt
// │
// ├── shared/                    # Código común para todas las automatizaciones (librerías, funciones compartidas)
// │   ├── utils/                 # Funciones o utilidades generales
// │   ├── config/                # Configuración global (API keys, rutas, etc.)
// │   └── README.md
// │
// ├── .gitignore                 # Archivos que no deseas incluir en el repositorio (logs, archivos temporales, etc.)
// ├── README.md                  # Documentación general del repositorio
// └── requirements.txt           # Dependencias generales para todas las automatizaciones (si aplica)
