import { useState } from 'react'
import DocumentUploader from './components/DocumentUploader'
import DocumentViewer from './components/DocumentViewer'
import SummaryPanel from './components/SummaryPanel'
import ChatInterface from './components/ChatInterface'

function App() {
  const [uploadedFile, setUploadedFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [ocrResult, setOcrResult] = useState(null)
  const [summaries, setSummaries] = useState(null)
  const [extracting, setExtracting] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)

  const handleFileUpload = (file) => {
    setUploadedFile(file)
    
    // Create image preview
    if (file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    } else {
      setImagePreview(null) // PDF preview not shown
    }
    
    // Reset results
    setOcrResult(null)
    setSummaries(null)
  }

  const handleExtractComplete = (result) => {
    setOcrResult(result)
  }

  const handleAnalysisComplete = (result) => {
    setSummaries(result)
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="container">
          <h1 className="app-title">Nepal Doc AI</h1>
          <p className="app-subtitle">Understand any Nepali document in seconds</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          
          {/* Upload Section */}
          {!ocrResult && (
            <DocumentUploader 
              onFileUpload={handleFileUpload}
              onExtractComplete={handleExtractComplete}
              onAnalysisComplete={handleAnalysisComplete}
              uploadedFile={uploadedFile}
              extracting={extracting}
              setExtracting={setExtracting}
              analyzing={analyzing}
              setAnalyzing={setAnalyzing}
            />
          )}

          {/* Two Column Layout - Document + Results */}
          {ocrResult && (
            <>
              <div className="document-layout">
                {/* Left: Document Viewer */}
                <DocumentViewer 
                  imagePreview={imagePreview}
                  fileName={uploadedFile?.name}
                  isPDF={uploadedFile?.type === 'application/pdf'}
                />

                {/* Right: Extracted Text + Summaries */}
                <div className="results-panel">
                  {/* OCR Stats */}
                  <div className="ocr-stats">
                    <div className="stat-item">
                      <span className="stat-label">Reading Quality</span>
                      <span className={`stat-value quality-${getQualityLevel(ocrResult.confidence_score)}`}>
                        {getQualityLabel(ocrResult.confidence_score)}
                      </span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Document Length</span>
                      <span className="stat-value">{ocrResult.word_count} words read</span>
                    </div>
                  </div>

                  {/* Extracted Text */}
                  <div className="extracted-text-section">
                    <h3 className="section-title">Extracted Text</h3>
                    <div className="extracted-text-box">
                      {ocrResult.cleaned_text}
                    </div>
                  </div>

                  {/* Summaries */}
                  {summaries && (
                    <SummaryPanel summaries={summaries} />
                  )}

                  {/* Loading state for analysis */}
                  {analyzing && (
                    <div className="loading-state">
                      <div className="spinner"></div>
                      <p>Analyzing document...</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Chat Interface */}
              {summaries && (
                <ChatInterface 
                  documentText={ocrResult.cleaned_text}
                />
              )}

              {/* Reset Button */}
              <div className="reset-section">
                <button 
                  className="btn-reset"
                  onClick={() => {
                    setUploadedFile(null)
                    setImagePreview(null)
                    setOcrResult(null)
                    setSummaries(null)
                  }}
                >
                  Upload Another Document
                </button>
              </div>
            </>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <p>Built for Nepali citizens</p>
          <p>Processing happens in your browser session — documents are not stored</p>
        </div>
      </footer>
    </div>
  )
}

// Helper functions
function getQualityLevel(confidence) {
  if (confidence >= 80) return 'excellent'
  if (confidence >= 50) return 'good'
  return 'fair'
}

function getQualityLabel(confidence) {
  if (confidence >= 80) return 'Excellent'
  if (confidence >= 50) return 'Good'
  return 'Fair — image may be unclear'
}

export default App
