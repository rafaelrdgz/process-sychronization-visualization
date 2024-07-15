import React, { useEffect, useRef } from 'react';
import "./Textarea.css"

const Textarea = ({ content }) => {
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.scrollTop = textareaRef.current.scrollHeight;
    }
  }, [content]);

  return (
    <textarea className='styled-textarea' ref={textareaRef} value={content} readOnly/>
  );
};

export default Textarea;
