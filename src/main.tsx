import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import DataPage from "./pages/dataUploadPage.jsx";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <DataPage />
  </StrictMode>,
)
