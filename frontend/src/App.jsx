import React, { useState } from 'react'
import UploadSection from './components/UploadSection'
import ResultsPanel from './components/ResultsPanel'
import './App.css'

function App() {
  const [analysisResults, setAnalysisResults] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)

  const handleAnalysisComplete = (results) => {
    setAnalysisResults(results)
    setIsAnalyzing(false)
  }

  const handleFileSelect = (file) => {
    setSelectedFile(file)
  }

  const handleReset = () => {
    setAnalysisResults(null)
    setSelectedFile(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">⚡</div>
            <h1>DPU Performance Studio</h1>
          </div>
          <p className="tagline">Audio-AI Workload Optimization Platform</p>
        </div>
      </header>

      <main className="app-main">
        {!analysisResults ? (
          <UploadSection
            onAnalysisComplete={handleAnalysisComplete}
            onFileSelect={handleFileSelect}
            isAnalyzing={isAnalyzing}
            setIsAnalyzing={setIsAnalyzing}
          />
        ) : (
          <ResultsPanel
            results={analysisResults}
            onReset={handleReset}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>© 2024 DPU Performance Studio. Software-first approach with CPU measurement and DPU simulation.</p>
      </footer>
    </div>
  )
}

export default App
