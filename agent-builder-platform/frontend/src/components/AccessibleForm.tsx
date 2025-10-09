import { TextField, FormHelperText, Box } from '@mui/material'
import { useState } from 'react'
import { generateAriaId } from '../utils/accessibility'

interface AccessibleTextFieldProps {
  label: string
  value: string
  onChange: (value: string) => void
  error?: string
  required?: boolean
  multiline?: boolean
  rows?: number
  placeholder?: string
  type?: string
}

export const AccessibleTextField = ({
  label,
  value,
  onChange,
  error,
  required = false,
  multiline = false,
  rows = 1,
  placeholder,
  type = 'text',
}: AccessibleTextFieldProps) => {
  const [fieldId] = useState(() => generateAriaId('field'))
  const [errorId] = useState(() => generateAriaId('error'))
  const [helperId] = useState(() => generateAriaId('helper'))

  return (
    <Box sx={{ mb: 2 }}>
      <TextField
        id={fieldId}
        label={label}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        error={Boolean(error)}
        required={required}
        multiline={multiline}
        rows={rows}
        placeholder={placeholder}
        type={type}
        fullWidth
        inputProps={{
          'aria-label': label,
          'aria-required': required,
          'aria-invalid': Boolean(error),
          'aria-describedby': error ? errorId : helperId,
        }}
      />
      {error && (
        <FormHelperText
          id={errorId}
          error
          role="alert"
          aria-live="polite"
        >
          {error}
        </FormHelperText>
      )}
    </Box>
  )
}

export default AccessibleTextField
