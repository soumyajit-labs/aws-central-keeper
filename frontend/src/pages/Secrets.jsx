import { useState, useEffect } from "react";
import { DEV_ENCR_TOKEN } from "../constants";
import { useNavigate } from "react-router-dom";
import api from "../api";

function strFormatter(str) {
    let t1 = str.replace('\\n', '\n');
    let t2 = t1.replace(/\\"!\[/, '"![');
    let t3 = t2.replace(/]\\"/, ']"');
    return t3;
}

function Secrets() {    
    const [vaultName, setVaultName] = useState("");
    const [encryptedVaultContent, setEncryptedVaultContent] = useState("");
    const getSecret = (e) => {
        api.get("/api/aws/secrets/fetch/?name=" + vaultName)
            .then((res) => res.data)
            .then((data) => { if (data == 400) {document.getElementById('yamlEncrypted').value = "Unhandled problem!"} else
                              if (data == 401) {document.getElementById('yamlEncrypted').value = "Not found!"}
                              else {setEncryptedVaultContent(data); console.log(encryptedVaultContent); 
                              document.getElementById('yamlEncrypted').value = strFormatter(data); }})
            .catch((err) => alert(err));
    };

    const postSecret = (e) => {
        e.preventDefault();
        api.post("/api/aws/secrets/upsert/", { 'name': vaultName, 'value': encryptedVaultContent })
            .then((res) => { if (res.data == 200) {document.getElementById('yamlEncrypted').value = "Vault updated!";} else
                             if (res.data == 201) {document.getElementById('yamlEncrypted').value = "Vault created!";}
                             else {document.getElementById('yamlEncrypted').value = "Unable to push through!";} })
            .catch((err) => alert(err));
    };

    const [decryptedVaultContent, setDecryptedVaultContent] = useState("");
    const [key, setKey] = useState("");
    const translate = (e, operation) => {
        let eKey = "";
        if (key) {eKey = key}
        else {eKey = DEV_ENCR_TOKEN}
        e.preventDefault();
        let content = "";
        if (operation == 'decrypt') { content = encryptedVaultContent; }
        else { content = decryptedVaultContent; }
        console.log({ 'text': content, 'operation': operation, 'key': eKey });
        
        api.post("/api/secrets/translate/raml/", { 'text': content, 'operation': operation, 'key': eKey })
           .then((res) => {
                console.log(res.statusText);
                if (operation == 'decrypt') { setDecryptedVaultContent(res.data['value']);
                                              document.getElementById('yamlDecrypted').value = strFormatter(res.data['value']); }
                else { setEncryptedVaultContent(res.data['value']);
                       document.getElementById('yamlEncrypted').value = strFormatter(res.data['value']); }
            })
            .catch((err) => alert(err));
    };

    let navigate = useNavigate();
    function logout() {
        localStorage.clear()
        navigate('/login');
    }

    return (
        <div>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1"></meta>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css"></link>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
            </head>
            <div class="row">
                <div class="col-sm-5">
                    <h2>AWS Key Vault</h2>
                </div>
                <div class="col-sm-3">
                    <br />
                <button class="btn btn-info glyphicon glyphicon-log-out" 
                        type="button" style={{"display": "block", "margin": "10 auto"}}
                        onClick={logout}>    Logout    </button>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-5">
                    <span>Encryption Key</span>
                </div>
                <div class="col-sm-1">
                    &nbsp;
                </div>
                <div class="col-sm-4">
                    <span>Vault Name</span>
                </div>
                <div class="col-sm-2">
                    &nbsp;
                </div>
            </div>
            <div class="row">
                <div class="col-sm-5">
                    <input id="encrKey" type="password" class="form-control" placeholder="Encryption Key" 
                     defaultValue={DEV_ENCR_TOKEN} onChange={(e) => setKey(e.target.value)}/>
                </div>
                <div class="col-sm-1">
                    &nbsp;
                </div>
                <div>
                    <div class="col-sm-4">
                        <input type="text" class="form-control" placeholder="Vault Name" onChange={(e) => setVaultName(e.target.value)}/>
                    </div>
                    <div class="col-sm-2">
                        <button class="btn btn-info glyphicon glyphicon-download event" type="button" onClick={() => {getSecret()}}> Download</button>
                    </div>
                </div>
                <hr/>
            </div>
            <div class="fluid-container">
                <div class="row">
                    <div class="col-sm-5">
                        <div class="input-group">
                            <textarea id="yamlDecrypted" rows="20" class="form-control" placeholder="Decrypted YAML" onChange={(e) => setDecryptedVaultContent(e.target.value)}></textarea>
                            <div class="input-group-addon">
                                <div class="glyphicon glyphicon-download event"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <button class="btn btn-info glyphicon glyphicon-arrow-right" type="button" onClick={(e) => translate(e, 'encrypt')}> Encrypt</button>
                        <hr></hr>
                        <button class="btn btn-info glyphicon glyphicon-arrow-left" type="button" onClick={(e) => translate(e, 'decrypt')}> Decrypt</button>
                    </div>
                    <div class="col-sm-6">
                        <div class="input-group">
                            <textarea id="yamlEncrypted" rows="20" class="form-control" placeholder="Encrypted YAML" onChange={(e) => setEncryptedVaultContent(e.target.value)}></textarea>
                            <div class="input-group-addon">
                                <div class="glyphicon glyphicon-download event"></div>
                            </div>
                        </div>
                        <br />
                        <div>
                            <button class="btn btn-info glyphicon glyphicon-cloud-upload" type="button" onClick={(e) => postSecret(e)}> Save</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Secrets;