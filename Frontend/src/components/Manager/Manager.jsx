import React, { useState } from 'react';
import './Manager.css';
import { Button, Stack, Typography } from '@mui/material';
import categoryConfig from './categoryConfig';

const roleIds = {
  administradores: 1,
  instructores: 2,
  alumnos: 3,
};

import { apiURL } from '../../const';
import { debounce } from 'lodash';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { CSSTransition } from 'react-transition-group';

const headers = {
  'Content-Type': 'application/json',
};

const convertSecondsToTime = (seconds) => {
  const hours = Math.floor(seconds / 3600).toString().padStart(2, '0');
  const minutes = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
  return `${hours}:${minutes}`;
};


const Modal = ({ isOpen, onClose, category }) => {
  const [step, setStep] = useState('selectAction');
  const [subStep, setSubStep] = useState('inputId');
  const [viewItems, setViewItems] = useState([]);
  const [formData, setFormData] = useState(() => {
    const initialData = {};
    if (categoryConfig[category.toLowerCase()]?.create) {
      categoryConfig[category.toLowerCase()].create.forEach(field => {
        initialData[field.key] = field.type === 'number' ? 0 : '';
      });
    }
    return initialData;
  });

  const handleClose = () => {
    setStep('selectAction');
    setFormData({});
    onClose();
  };

  const handleShowById = async () => {
    try {
      let url = `${apiURL}${category.toLowerCase()}`;
      if (['alumnos', 'instructores', 'administradores'].includes(category.toLowerCase())) {
        url = `${apiURL}personas`;
      }
      console.log('Fetching data from:', url);
      const response = await fetch(url, {
        headers,
        method: 'GET',
      });
      if (response.ok) {
        let data = await response.json();
  
        // Convertir los campos de tiempo si existen
        if (Array.isArray(data)) {
          data = data.map((item) => {
            categoryConfig[category.toLowerCase()]?.modify.forEach(field => {
              if (field.type === 'time' && typeof item[field.key] === 'number') {
                item[field.key] = convertSecondsToTime(item[field.key]);
              }
            });
            return item;
          });
        } else {
          categoryConfig[category.toLowerCase()]?.modify.forEach(field => {
            if (field.type === 'time' && typeof data[field.key] === 'number') {
              data[field.key] = convertSecondsToTime(data[field.key]);
            }
          });
        }
  
        setStep('viewItems');
        setViewItems(Array.isArray(data) ? data : []);
      } else {
        toast.error('No se pudieron obtener los elementos del servidor.');
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error('Error al conectar con el servidor, por favor intenta nuevamente más tarde.');
    }
  };
  
  

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'number' ? parseFloat(value) || 0 : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Asignar id_rol si se está creando o modificando un usuario de tipo alumno, instructor o administrador
    if (['alumnos', 'instructores', 'administradores'].includes(category.toLowerCase())) {
      formData.id_rol = roleIds[category.toLowerCase()];
    }
  
    if (formData.ci && !/^[0-9]{8}$/.test(formData.ci)) {
      toast.error('El campo CI debe tener exactamente 8 dígitos');
      return;
    }
  
    console.log('Submitting form with data:', formData);
  
    try {
      let response;
      let url = `${apiURL}${category.toLowerCase()}`;
      if (['alumnos', 'instructores', 'administradores'].includes(category.toLowerCase())) {
        url = `${apiURL}personas`;
      }
      if (step === 'modify' || step === 'delete') {
        //add the first field's value to the url
        url = `${url}/${formData[categoryConfig[category.toLowerCase()][step][0].key]}`;
      }
  
      let options = {
        headers,
        mode: 'cors',
      };
  
      switch (step) {
        case 'create':
          response = await fetch(url, {
            ...options,
            method: 'POST',
            body: JSON.stringify(formData),
          });
          break;
        case 'modify':
          if (subStep === 'inputId') {
            response = await fetch(url, {
              ...options,
              method: 'GET',
            });
            if (response.ok) {
              const data = await response.json();
              setFormData(data);
              setSubStep('modifyFields');
            } else {
              const errorData = await response.json();
              console.error('Error fetching data:', errorData);
              toast.error('No se pudo obtener la información del registro, verifica el CI.');
            }
            return;
          }
          response = await fetch(url, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(formData),
          });
          break;
        case 'delete':
          response = await fetch(url, {
            ...options,
            method: 'DELETE',
          });
          break;
        default:
          console.error('Unsupported action');
          return;
      }
  
      if (response.ok) {
        toast.success('Acción completada con éxito');
        handleClose();
      } else {
        const errorData = await response.json();
        console.error('Error Response Data:', errorData);
        toast.error(`Error: ${errorData.detail || 'Error al realizar la acción, por favor verifica los datos'}`);
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error('Error al conectar con el servidor, por favor intenta nuevamente más tarde.');
    }
  };
  

  const renderContent = () => {
    if (step === 'selectAction') {
      return (
        <div className="category-management-container">
  <Typography variant="h4" gutterBottom className="category-title">
    Gestionar {category}
  </Typography>
  <Stack direction="row" spacing={5} className="category-buttons">
    <Button 
      variant="contained" 
      color="primary" 
      onClick={() => setStep('create')}
    >
      Crear {category}
    </Button>
    <Button 
      variant="outlined" 
      color="primary" 
      onClick={() => setStep('modify')}
    >
      Modificar {category}
    </Button>
    <Button 
      variant="contained" 
      color="secondary" 
      onClick={() => setStep('delete')}
    >
      Eliminar {category}
    </Button>
  </Stack>
</div>

      );
    }
  
    if (step === 'modify' && subStep === 'inputId') {
      const firstField = categoryConfig[category.toLowerCase()]?.modify[0];
      return (
        <div>
          <h2>Modificar {category}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <label>{firstField?.label}</label>
              <input
                type={firstField?.type}
                name={firstField?.key}
                placeholder={firstField?.label}
                value={formData[firstField?.key] || ''}
                onChange={handleInputChange}
              />
            </div>
            <button type="submit">Enviar</button>
          </form>
          <Button
  onClick={handleShowById}
  variant="contained"
  className="admin-button send-button"
>
  Mostrar todos los elementos
</Button>

<Button
  onClick={() => setStep('selectAction')}
  variant="outlined"
  className="back-button"
>
  Atrás
</Button>

        </div>
      );
    }
    

    if (step === 'viewItems') {
      return (
        <div className="modal-scrollable">
          <h2>Lista de {category}</h2>
          <ul>
            {viewItems.length > 0 ? (
              viewItems.map((item) => (
                <li
                  key={item.id}
                  onClick={() => {
                    setFormData(item); // Configura los datos del formulario con el elemento seleccionado
                    setSubStep('modifyFields'); // Cambia al segundo sub-paso de modificación
                    setStep('modify'); // Asegúrate de estar en el paso de modificar
                  }}
                  style={{ cursor: 'pointer', padding: '0.5rem', borderBottom: '1px solid #ccc' }} // Añadir estilo para que parezca clicable
                >
                  {Object.entries(item).map(([key, value]) => (
                    <div key={key}>
                      <strong>{key}:</strong> {value}
                    </div>
                  ))}
                </li>
              ))
            ) : (
              <li>No se encontraron elementos</li>
            )}
          </ul>
          <button onClick={() => setStep('selectAction')}>Atrás</button>
        </div>
      );
    }
    
  
    const fields = categoryConfig[category.toLowerCase()]?.[step];
  
    if (!fields || fields.length === 0) {
      return (
        <div>
          <p>No se encontraron campos para {step} {category}.</p>
          <button onClick={() => setStep('selectAction')}>Atrás</button>
        </div>
      );
    }
  
    return (
      <div>
        <h2>{step === 'create' ? 'Crear' : step === 'modify' ? 'Modificar' : 'Eliminar'} {category}</h2>
        <form onSubmit={handleSubmit}>
          {fields.map((field) => (
            <div key={field.key} className="form-row">
              <label>{field.label}</label>
              <input
                type={field.type}
                name={field.key}
                placeholder={field.label}
                value={formData[field.key] || ''}
                onChange={handleInputChange}
              />
            </div>
          ))}
          <button type="submit">Enviar</button>
        </form>
        <button onClick={() => setStep('selectAction')}>Atrás</button>
      </div>
    );
  };
  

  return (
    <CSSTransition in={isOpen} timeout={300} classNames="modal" unmountOnExit>
      <div className="modal-backdrop">
        <div className="modal">
        <Button
  onClick={handleClose}
  variant="contained"
  color="primary"
  className="close-button"
  style={{ minWidth: '40px', minHeight: '40px', position: 'absolute', top: '0', right: '0' }}
>
  X
</Button>

          {renderContent()}
        </div>
      </div>
    </CSSTransition>
  );
};

const Manager = ({ category }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div>
      <Button
  variant="contained"
  className="admin-button"
  onClick={() => setIsModalOpen(true)}
>
  Gestionar {category}
</Button>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} category={category} />
    </div>
  );
};

export default Manager
