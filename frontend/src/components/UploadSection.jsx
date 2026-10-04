import React, { useRef } from 'react'
import axios from 'axios'
import { Upload, Zap, Cpu, Cpu as DpuIcon } from 'lucide-react'
import './UploadSection.css'

function UploadSection({ onAnalysisComplete, onFileSelect, isAnalyzing, setIsAnalyzing }) {
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      onFileSelect(file)
    }
  }

  const handleUpload = async () => {
    const file = fileInputRef.current?.files[0]
    if (!file) {
      alert('Please select an audio file first')
      return
    }

    setIsAnalyzing(true)

    const formData = new FormData()
    formData.append('audio_file', file)

    try {
      const response = await axios.post('http://localhost:8000/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      onAnalysisComplete(response.data)
    } catch (error) {
      console.error('Analysis failed:', error)
      alert('Analysis failed. Please try again.')
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="upload-section">
      <div className="upload-card">
        <div className="upload-header">
          <h2>Analyze Audio-AI Workload</h2>
          <p>Upload an audio file to analyze performance and get optimization recommendations</p>
        </div>

        <div className="upload-area">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="audio/*"
            id="audio-upload"
            className="file-input"
          />
          <label htmlFor="audio-upload" className="upload-label">
            <Upload className="upload-icon" size={48} />
            <div className="upload-text">
              <p className="upload-main-text">Click to upload or drag and drop</p>
              <p className="upload-subtext">Audio files (WAV, MP3, FLAC, etc.)</p>
            </div>
          </label>
        </div>

        <button
          onClick={handleUpload}
          disabled={isAnalyzing}
          className={`analyze-button ${isAnalyzing ? 'analyzing' : ''}`}
        >
          {isAnalyzing ? (
            <>
              <span className="spinner"></span>
              Analyzing...
            </>
          ) : (
            <>
              <Zap size={20} />
              Start Analysis
            </>
          )}
        </button>

        <div className="info-cards">
          <div className="info-card">
            <Cpu className="info-icon" size={32} />
            <h3>CPU Baseline</h3>
            <p>Measure performance on CPU</p>
          </div>
          <div className="info-card">
            <DpuIcon className="info-icon" size={32} />
            <h3>DPU Simulation</h3>
            <p>Simulate DPU acceleration</p>
          </div>
          <div className="info-card">
            <Zap className="info-icon" size={32} />
            <h3>Optimization</h3>
            <p>Get intelligent recommendations</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UploadSection
