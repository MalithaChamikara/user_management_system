'use client' // This is a client component
import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import axios from 'axios'
import {
    TextField,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    MenuItem,
    Select,
    InputLabel,
    FormControl,
} from '@mui/material'


export default function UserCreationForm() {

    const dispatch = useDispatch() // Initialize the Redux dispatch function
    const [firstName, setFirstName] = useState('')
    const [lastName, setLastName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [dateOdBirth, setDateOfBirth] = useState('')
    const [roleTypeId, setRoleTypeId] = useState(0)
    const [statusId, setStatusId] = useState(0)
    const [roleTypes, setRoleTypes] = useState([])
    const [statuses, setStatuses] = useState([])

    // Fetch role types and statuses from the API when the component mounts
    useEffect(() => {
        if (open) {
            fetchRoleTypes()
            fetchStatuses()
        }
    }, [open])

    // Fetch role types from the API
    const fetchRoleTypes = async () => {
        try {
            const response = await axios.get(`${API_URL}/roles`, {
                headers: {
                    Authorization: `Bearer ${sessionStorage.getItem('token')}`
                }
            })
            setRoleTypes(response.data)
        } catch (error) {
            console.error('Error fetching role types:', error)
        }
    }

    // Fetch statuses from the API
    const fetchStatuses = async () => {
        try {
            const response = await axios.get(`${API_URL}/statuses`, {
                headers: {
                    Authorization: `Bearer ${sessionStorage.getItem('token')}`
                }
            })
            setStatuses(response.data)
        } catch (error) {
            console.error('Error fetching statuses:', error)
        }
    }

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault()
        const formData = {
            FirstName: firstName,
            LastName: lastName,
            Email: email,
            Password: password,
            DateOfBirth: dateOdBirth,
            roleType_id: roleTypeId,
            status_id: statusId,
        }

        try {
            const response = await axios.post(`${API_URL}/users`, formData, {
                headers: {
                    Authorization: `Bearer ${sessionStorage.getItem('token')}`
                }
            })
            handleClose()
            setFirstName('')
            setLastName('')
            setEmail('')
            setPassword('')
            setDateOfBirth('')
            setRoleTypeId(0)
            setStatusId(0)
        } catch (error) {
            console.error('Error creating user:', error)
        }

    }

    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>Create User</DialogTitle>
            <DialogContent>
                <form onSubmit={handleSubmit}>
                    <TextField
                        label="First Name"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        label="Last Name"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        label="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        label="Password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        label="Date of Birth"
                        type="date"
                        value={dateOdBirth}
                        onChange={(e) => setDateOfBirth(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Role Type</InputLabel>
                        <Select
                            value={roleTypeId}
                            onChange={(e) => setRoleTypeId(e.target.value)}
                            label="Role Type"
                            fullWidth
                            margin="normal"
                        >
                            {roleTypes.map((role) => (
                                <MenuItem key={role.id} value={role.id}>
                                    {role.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Status</InputLabel>
                        <Select
                            value={statusId}
                            onChange={(e) => setStatusId(e.target.value)}
                            label="Status"
                            fullWidth
                            margin="normal"
                        >
                            {statuses.map((status) => (
                                <MenuItem key={status.id} value={status.id}>
                                    {status.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <DialogActions>
                        <Button onClick={handleClose} color="primary">
                            Cancel
                        </Button>
                        <Button type="submit" color="primary">
                            Create User
                        </Button>
                    </DialogActions>
                </form>
            </DialogContent>
        </Dialog>

    )
}
