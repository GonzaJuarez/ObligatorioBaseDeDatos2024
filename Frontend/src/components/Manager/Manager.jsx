import React, { useState } from 'react';
import './Manager.css';
import categoryConfig from './categoryConfig'; // Importar la configuración de categorías
import { apiURL } from '../../const';
import { debounce } from 'lodash';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { CSSTransition } from 'react-transition-group';

const headers = {
  'Content-Type': 'application/json',
};

const Modal = ({ isOpen, onClose, category }) => {
  const [step, setStep] = useState('selectAction'); // Mantiene el seguimiento de la parte del modal en la que se encuentra el usuario
  const [formData, setFormData] = useState({}); // Estado para manejar los datos del formulario

  const handleClose = () => {
    setStep('selectAction'); // Restablece el paso al cerrar el modal
    setFormData({}); // Limpiar el formulario al cerrar el modal
    onClose();
  };

  const handleInputChange = debounce((e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  }, 300);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let response;
      let url = `${apiURL}/personas`.replace(/([^:]\/)\/+/g, "$1");

      if (['Alumnos', 'Instructores', 'Administradores'].includes(category.toLowerCase()) && step === 'create') {
        formData.id_rol = category.slice(0, -1); // Assign role based on category
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
          if (!formData.ci) {
            toast.error('El CI es obligatorio para modificar un registro');
            return;
          }
          response = await fetch(`${url}/${formData.ci}`, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(formData),
          });
          break;
        case 'delete':
          if (!formData.ci) {
            toast.error('El CI es obligatorio para eliminar un registro');
            return;
          }
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

export default Manager;
