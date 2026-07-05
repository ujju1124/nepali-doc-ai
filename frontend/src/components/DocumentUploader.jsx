import { useState } from 'react'
import { Upload, FileText } from 'lucide-react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function DocumentUploader({ 
  onFileUpload, 
  onExtractComplete, 
  onAnalysisComplete,
  uploadedFile,
  extracting,
  setExtracting,
  analyzing,
  setAnalyzing
}) {
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = (file) => {
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf']
    if (!allowedTypes.includes(file.type)) {
      setError('Please upload a JPG, PNG, or PDF file')
      return
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB')
      return
    }

    setError(null)
    onFileUpload(file)
  }

  const handleExtractAndAnalyze = async () => {
    if (!uploadedFile) return

    setError(null)
    setExtracting(true)

    try {
      // Step 1: Extract text
      const formData = new FormData()
      formData.append('file', uploadedFile)

      const extractResponse = await axios.post(`${API_URL}/extract`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      const ocrResult = extractResponse.data

      if (!ocrResult.success) {
        throw new Error(ocrResult.error || 'OCR extraction failed')
      }

      if (ocrResult.word_count === 0) {
        throw new Error('No text detected in the document. Please upload a clearer image.')
      }

      onExtractComplete(ocrResult)
      setExtracting(false)

      // Step 2: Analyze text
      setAnalyzing(true)

      const analyzeResponse = await axios.post(`${API_URL}/analyze`, {
        text: ocrResult.cleaned_text
      })

      const analysisResult = analyzeResponse.data

      if (!analysisResult.success) {
        throw new Error(analysisResult.error || 'Analysis failed')
      }

      onAnalysisComplete(analysisResult)
      setAnalyzing(false)

    } catch (err) {
      setExtracting(false)
      setAnalyzing(false)
      
      if (err.response) {
        setError(err.response.data.detail || 'Server error occurred')
      } else if (err.request) {
        setError('Could not connect to server. Make sure the backend is running.')
      } else {
        setError(err.message)
      }
    }
  }

  return (
    <div className="uploader-section">
      <div 
        className={`upload-zone ${dragActive ? 'drag-active' : ''} ${uploadedFile ? 'has-file' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {!uploadedFile ? (
          <>
            <Upload className="upload-icon" size={48} />
            <h3 className="upload-title">Upload Your Document</h3>
            <p className="upload-description">
              Drag and drop or click to browse
            </p>
            <p className="upload-formats">JPG, PNG, or PDF • Max 10MB</p>
            <input
              type="file"
              id="file-upload"
              className="file-input"
              accept=".jpg,.jpeg,.png,.pdf"
              onChange={handleChange}
            />
            <label htmlFor="file-upload" className="btn-upload">
              Read Document
            </label>
          </>
        ) : (
          <>
            <FileText className="file-icon" size={48} />
            <p className="file-name">{uploadedFile.name}</p>
            <p className="file-size">
              {(uploadedFile.size / 1024).toFixed(1)} KB
            </p>
            <button 
              className="btn-extract"
              onClick={handleExtractAndAnalyze}
              disabled={extracting || analyzing}
            >
              {extracting ? 'Reading document...' : analyzing ? 'Analyzing...' : 'Extract & Analyze'}
            </button>
            <button 
              className="btn-change"
              onClick={() => onFileUpload(null)}
              disabled={extracting || analyzing}
            >
              Change File
            </button>
          </>
        )}
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}
    </div>
  )
}

export default DocumentUploader
