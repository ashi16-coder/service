import { useState } from "react";
import { Link } from "react-router-dom";
import { MapPin, Mail, ArrowLeft, CheckCircle } from "lucide-react";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);

  return (
    <div style={S.page}>
      <div style={S.card}>
        <div style={S.logo}><div style={S.logoIcon}><MapPin size={20} color="#fff"/></div><span style={{fontWeight:700,fontSize:18}}>TourGuide</span></div>
        {!sent ? (
          <>
            <h2 style={S.title}>Forgot Password?</h2>
            <p style={S.sub}>Enter your registered email and we'll send a reset link.</p>
            <form onSubmit={(e)=>{e.preventDefault();if(email)setSent(true);}} style={S.form}>
              <div style={S.wrap}><Mail size={16} style={S.icon}/><input type="email" placeholder="Enter your email" value={email} onChange={e=>setEmail(e.target.value)} style={S.input} required/></div>
              <button type="submit" style={S.btn}>Send Reset Link</button>
            </form>
          </>
        ) : (
          <div style={S.success}>
            <CheckCircle size={40} color="#22c55e"/>
            <h3 style={{fontWeight:700,fontSize:18}}>Check your email!</h3>
            <p style={{color:"#64748b",fontSize:14}}>A reset link was sent to <strong>{email}</strong></p>
          </div>
        )}
        <Link to="/login" style={S.back}><ArrowLeft size={15}/> Back to Login</Link>
      </div>
    </div>
  );
}

const S = {
  page:{minHeight:"100vh",display:"flex",alignItems:"center",justifyContent:"center",background:"#f8fafc"},
  card:{background:"#fff",borderRadius:20,padding:40,width:420,boxShadow:"0 4px 24px rgba(0,0,0,0.08)",display:"flex",flexDirection:"column",gap:16},
  logo:{display:"flex",alignItems:"center",gap:10,marginBottom:8},
  logoIcon:{width:38,height:38,borderRadius:10,background:"#2563eb",display:"flex",alignItems:"center",justifyContent:"center"},
  title:{fontSize:22,fontWeight:800,color:"#1e293b"},
  sub:{fontSize:14,color:"#64748b",lineHeight:1.6},
  form:{display:"flex",flexDirection:"column",gap:14},
  wrap:{position:"relative",display:"flex",alignItems:"center"},
  icon:{position:"absolute",left:12,color:"#94a3b8"},
  input:{width:"100%",padding:"11px 14px 11px 38px",border:"1.5px solid #e2e8f0",borderRadius:8,fontSize:14,outline:"none"},
  btn:{padding:13,background:"linear-gradient(135deg,#2563eb,#0ea5e9)",color:"#fff",border:"none",borderRadius:10,fontWeight:700,fontSize:15,cursor:"pointer"},
  success:{display:"flex",flexDirection:"column",alignItems:"center",gap:12,padding:"20px 0",textAlign:"center"},
  back:{display:"flex",alignItems:"center",gap:6,color:"#2563eb",fontWeight:600,fontSize:14,marginTop:4},
};
