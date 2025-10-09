import { Box, Link } from '@mui/material'

interface SkipLinkProps {
  href: string
  children: React.ReactNode
}

export const SkipLink = ({ href, children }: SkipLinkProps) => {
  return (
    <Link
      href={href}
      sx={{
        position: 'absolute',
        left: '-9999px',
        zIndex: 9999,
        padding: '1rem',
        backgroundColor: 'primary.main',
        color: 'primary.contrastText',
        textDecoration: 'none',
        '&:focus': {
          left: '50%',
          top: '1rem',
          transform: 'translateX(-50%)',
        },
      }}
    >
      {children}
    </Link>
  )
}

export const SkipLinks = () => {
  return (
    <Box component="nav" aria-label="Skip links">
      <SkipLink href="#main-content">Skip to main content</SkipLink>
      <SkipLink href="#navigation">Skip to navigation</SkipLink>
    </Box>
  )
}

export default SkipLinks
