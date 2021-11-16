from OpenSSL import SSL
import idna

from socket import socket


class CertificateService:

    def get_certificate(self, hostname, port):
        try:
            certificate = dict()
            hostname_idna = idna.encode(hostname)
            sock = socket()
    
            sock.connect((hostname, port))
            peername = sock.getpeername()
            ctx = SSL.Context(SSL.SSLv23_METHOD)  # most compatible
            ctx.check_hostname = False
            ctx.verify_mode = SSL.VERIFY_NONE
    
            sock_ssl = SSL.Connection(ctx, sock)
            sock_ssl.set_connect_state()
            sock_ssl.set_tlsext_host_name(hostname_idna)
            sock_ssl.do_handshake()
            cert = sock_ssl.get_peer_certificate()
            crypto_cert = cert.to_cryptography()
            sock_ssl.close()
            sock.close()
    
            dics = dict()
            attributes = crypto_cert.issuer
            for attribute in attributes:
                dics[attribute.oid._name] = attribute.value
    
            certificate['validate'] = crypto_cert.not_valid_after.strftime('%Y-%m-%d')
            certificate['cert'] = dics
            certificate['hostname'] = hostname
            certificate['peername'] = peername
            return certificate
        except Exception as e:
            print('Erro ao recuperar o certificado')
            e.with_traceback()
            pass
