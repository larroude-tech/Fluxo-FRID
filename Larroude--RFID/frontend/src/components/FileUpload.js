import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Upload, FileSpreadsheet, AlertCircle } from 'lucide-react';
import { toast } from 'react-toastify';

const FileUpload = ({ onFileUpload }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const processFile = useCallback(async (file) => {
    setIsUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('excel', file);

      const response = await axios.post('/api/upload-excel', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          console.log(`Upload progress: ${percentCompleted}%`);
        },
      });

      if (response.data && response.data.data) {
        onFileUpload(response.data.data);
      } else {
        throw new Error('Resposta inválida do servidor');
      }
    } catch (error) {
      console.error('Erro no upload:', error);
      const errorMessage = error.response?.data?.error || 'Erro ao processar arquivo';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsUploading(false);
    }
  }, [onFileUpload]);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      const error = rejectedFiles[0].errors[0];
      setError(`Arquivo rejeitado: ${error.message}`);
      toast.error(`Arquivo rejeitado: ${error.message}`);
      return;
    }

    if (acceptedFiles.length > 0) {
      processFile(acceptedFiles[0]);
    }
  }, [processFile]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv']
    },
    maxFiles: 1,
    disabled: isUploading
  });

  return (
    <div className="card">
      <div
        {...getRootProps()}
        className={`upload-zone ${
          isDragActive ? 'dragover' : ''
        } ${
          isDragReject ? 'drag-reject' : ''
        } ${
          isUploading ? 'uploading' : ''
        }`}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <div className="upload-content">
            <div className="spinner"></div>
            <div className="upload-text">Processando arquivo...</div>
            <div className="upload-subtext">Por favor, aguarde</div>
          </div>
        ) : (
          <div className="upload-content">
            {isDragActive ? (
              <>
                <Upload className="upload-icon" size={48} />
                <div className="upload-text">Solte o arquivo aqui...</div>
              </>
            ) : (
              <>
                <FileSpreadsheet className="upload-icon" size={48} />
                <div className="upload-text">
                  Arraste e solte seu arquivo Excel ou CSV aqui
                </div>
                <div className="upload-subtext">
                  ou clique para selecionar um arquivo (.xlsx, .xls, .csv)
                </div>
              </>
            )}
          </div>
        )}
      </div>

      {error && (
        <div className="error">
          <AlertCircle size={16} />
          {error}
        </div>
      )}

      <div className="info">
        <h4>Formato esperado do arquivo Excel/CSV:</h4>
        <ul>
          <li><strong>STYLE_NAME:</strong> Nome do estilo do produto</li>
          <li><strong>VPM:</strong> Código VPM do produto</li>
          <li><strong>COLOR:</strong> Cor do produto</li>
          <li><strong>SIZE:</strong> Tamanho do produto</li>
        </ul>
        <p><small>Certifique-se de que seu arquivo Excel ou CSV contém essas colunas na primeira linha.</small></p>
      </div>
    </div>
  );
};

export default FileUpload;