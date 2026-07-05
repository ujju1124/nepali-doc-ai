import { FileText } from 'lucide-react'

function DocumentViewer({ imagePreview, fileName, isPDF }) {
  return (
    <div className="document-viewer">
      <h3 className="section-title">Uploaded Document</h3>
      <div className="document-preview">
        {imagePreview ? (
          <img 
            src={imagePreview} 
            alt={fileName}
            className="document-image"
          />
        ) : isPDF ? (
          <div className="pdf-placeholder">
            <FileText size={64} />
            <p className="pdf-name">{fileName}</p>
            <p className="pdf-note">First page processed</p>
          </div>
        ) : (
          <div className="no-preview">
            <p>No preview available</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default DocumentViewer
