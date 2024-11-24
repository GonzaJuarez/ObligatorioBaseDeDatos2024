import React, { useState } from 'react';
import './Manager.css';
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
      const url = `${apiURL}${category.toLowerCase()}`;
      console.log('Fetching data from:', url);
      const response = await fetch(url, {
        headers,
        method: 'GET',
      });
      if (response.ok) {
        const data = await response.json();
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
    if (['alumnos', 'instructores', 'administradores'].includes(category.toLowerCase()) && step === 'create') {
      formData.id_rol = roleIds[category.toLowerCase()];
    }
    if (formData.ci && !/^[0-9]{8}$/.test(formData.ci)) {
      toast.error('El campo CI debe tener exactamente 8 dígitos');
      return;
    }
    console.log('Submitting form with data:', formData);
    try {
      let response;
      const url = `${apiURL}/personas/${step === 'delete' ? formData.ci : ''}`.replace(/\/\/+/, '/');

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
            response = await fetch(`${url}/${formData.ci}`, {
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
          response = await fetch(`${url}/${formData.ci}`, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(formData),
          });
          break;
        case 'delete':
          response = await fetch(`${url}/${formData.ci}`, {
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
        <div>
          <h2>Gestionar {category}</h2>
          <button onClick={() => setStep('create')}>Crear {category}</button>
          <button onClick={() => setStep('modify')}>Modificar {category}</button>
          <button onClick={() => setStep('delete')}>Eliminar {category}</button>
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
          <button onClick={handleShowById}>Mostrar todos los elementos</button>
          <button onClick={() => setStep('selectAction')}>Atrás</button>
        </div>
      );
    }
    

    if (step === 'viewItems') {
      return (
        <div>
          <h2>Lista de {category}</h2>
          <ul>
            {viewItems.length > 0 ? (
              viewItems.map((item) => (
                <li key={item.id}>
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
          <button className="close-button" onClick={handleClose}>X</button>
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
      <button onClick={() => setIsModalOpen(true)}>Gestionar {category}</button>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} category={category} />
    </div>
  );
};

export default Manager
