import { configureStore } from "@reduxjs/toolkit";

import userReducer from './userSlice'
import authReducer from './authSlice'

// create  and configure the redux store
export const store = configureStore({
    reducer:{
        users:userReducer,
        auth:authReducer
    }
})