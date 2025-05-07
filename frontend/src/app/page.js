'use client'
import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useRouter } from 'next/navigation'
import axios from 'axios'
import UserCreationForm from '../components/UserCreationForm'
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  Box 
} from '@mui/material'


export default function page() {
  const dispatch = useDispatch() // Initialize the Redux dispatch function
  const router = useRouter() // Initialize the Next.js router for navigation between pages
  return (
    <div>
      
    </div>
  )
}
