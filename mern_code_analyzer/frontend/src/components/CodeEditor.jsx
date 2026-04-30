import React, { useContext } from 'react';
import Editor from '@monaco-editor/react';
import { ThemeContext } from '../context/ThemeContext';

export default function CodeEditor({ code, onChange, language }) {
  const { isDark } = useContext(ThemeContext);

  const handleEditorChange = (value) => {
    onChange(value);
  };

  return (
    <Editor
      height="100%"
      language={language === 'cpp' ? 'cpp' : language}
      theme={isDark ? "vs-dark" : "vs"}
      value={code}
      onChange={handleEditorChange}
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        padding: { top: 16, bottom: 16 },
        scrollBeyondLastLine: false,
        smoothScrolling: true,
        cursorBlinking: "smooth",
        fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
      }}
      loading={
        <div className="flex justify-center items-center h-full text-gray-500">
          Loading editor...
        </div>
      }
    />
  );
}
