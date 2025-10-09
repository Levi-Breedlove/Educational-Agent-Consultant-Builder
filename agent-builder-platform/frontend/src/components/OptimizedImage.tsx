import React, { useState, useEffect, useRef } from 'react'
import { Box, Skeleton } from '@mui/material'

/**
 * Optimized image component with lazy loading and responsive images
 * 
 * Requirements: 12.2
 */
export interface OptimizedImageProps {
  src: string
  alt: string
  width?: number | string
  height?: number | string
  aspectRatio?: string
  objectFit?: 'contain' | 'cover' | 'fill' | 'none' | 'scale-down'
  loading?: 'lazy' | 'eager'
  placeholder?: 'blur' | 'skeleton' | 'none'
  blurDataURL?: string
  sizes?: string
  srcSet?: string
  onLoad?: () => void
  onError?: () => void
  className?: string
  style?: React.CSSProperties
}

/**
 * Optimized Image Component
 * 
 * Features:
 * - Lazy loading with Intersection Observer
 * - Responsive images with srcSet
 * - Blur placeholder while loading
 * - Automatic aspect ratio preservation
 * - Error handling with fallback
 */
export const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  width = '100%',
  height = 'auto',
  aspectRatio,
  objectFit = 'cover',
  loading = 'lazy',
  placeholder = 'skeleton',
  blurDataURL,
  sizes,
  srcSet,
  onLoad,
  onError,
  className,
  style,
}) => {
  const [isLoaded, setIsLoaded] = useState(false)
  const [hasError, setHasError] = useState(false)
  const [isInView, setIsInView] = useState(loading === 'eager')
  const imgRef = useRef<HTMLImageElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  // Intersection Observer for lazy loading
  useEffect(() => {
    if (loading === 'eager' || !containerRef.current) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsInView(true)
            observer.disconnect()
          }
        })
      },
      {
        rootMargin: '50px', // Start loading 50px before entering viewport
      }
    )

    observer.observe(containerRef.current)

    return () => observer.disconnect()
  }, [loading])

  // Handle image load
  const handleLoad = () => {
    setIsLoaded(true)
    onLoad?.()
  }

  // Handle image error
  const handleError = () => {
    setHasError(true)
    onError?.()
  }

  // Calculate container style
  const containerStyle: React.CSSProperties = {
    position: 'relative',
    width,
    height: aspectRatio ? 0 : height,
    paddingBottom: aspectRatio ? `calc(100% / (${aspectRatio}))` : undefined,
    overflow: 'hidden',
    ...style,
  }

  // Calculate image style
  const imageStyle: React.CSSProperties = {
    position: aspectRatio ? 'absolute' : 'relative',
    top: 0,
    left: 0,
    width: '100%',
    height: aspectRatio ? '100%' : 'auto',
    objectFit,
    opacity: isLoaded ? 1 : 0,
    transition: 'opacity 0.3s ease-in-out',
  }

  return (
    <Box
      ref={containerRef}
      sx={containerStyle}
      className={className}
    >
      {/* Placeholder */}
      {!isLoaded && !hasError && (
        <>
          {placeholder === 'skeleton' && (
            <Skeleton
              variant="rectangular"
              width="100%"
              height="100%"
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
              }}
            />
          )}
          {placeholder === 'blur' && blurDataURL && (
            <img
              src={blurDataURL}
              alt=""
              aria-hidden="true"
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                objectFit,
                filter: 'blur(10px)',
                transform: 'scale(1.1)',
              }}
            />
          )}
        </>
      )}

      {/* Actual image */}
      {isInView && !hasError && (
        <img
          ref={imgRef}
          src={src}
          srcSet={srcSet}
          sizes={sizes}
          alt={alt}
          loading={loading}
          onLoad={handleLoad}
          onError={handleError}
          style={imageStyle}
        />
      )}

      {/* Error fallback */}
      {hasError && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: 'rgba(0, 0, 0, 0.1)',
            color: 'text.secondary',
            fontSize: '0.875rem',
          }}
        >
          Failed to load image
        </Box>
      )}
    </Box>
  )
}

/**
 * Generate srcSet for responsive images
 */
export function generateSrcSet(
  baseUrl: string,
  widths: number[]
): string {
  return widths
    .map(width => `${baseUrl}?w=${width} ${width}w`)
    .join(', ')
}

/**
 * Generate sizes attribute for responsive images
 */
export function generateSizes(
  breakpoints: Array<{ maxWidth: string; size: string }>
): string {
  return breakpoints
    .map(bp => `(max-width: ${bp.maxWidth}) ${bp.size}`)
    .join(', ')
}

export default OptimizedImage
