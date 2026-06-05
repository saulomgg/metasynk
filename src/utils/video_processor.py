import os
import subprocess
import ffmpeg

def get_metadata(video_path):
    """Lê os metadados de um arquivo de vídeo usando ffmpeg-python."""
    try:
        probe = ffmpeg.probe(video_path)
        return probe
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if hasattr(e, 'stderr') and e.stderr else str(e)
        raise Exception(f"Erro FFmpeg ao ler metadados: {error_message}")
    except Exception as e:
        raise Exception(f"Erro inesperado ao ler metadados: {e}")

def remove_all_metadata(video_path, output_path):
    """Remove todos os metadados de um vídeo."""
    try:
        ffmpeg.input(video_path).output(output_path, map_metadata=-1, c="copy").run(overwrite_output=True)
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if hasattr(e, 'stderr') and e.stderr else str(e)
        raise Exception(f"Erro FFmpeg ao remover metadados: {error_message}")

def insert_custom_metadata(video_path, output_path, metadata_dict):
    """Insere metadados personalizados em um vídeo."""
    import tempfile
    
    try:
        # Cria um arquivo temporário com os metadados no formato FFMETADATA
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as metadata_file:
            metadata_file.write(";FFMETADATA1\n")
            for key, value in metadata_dict.items():
                # Escapa caracteres especiais conforme padrão FFmpeg
                escaped_value = value.replace('=', '\\=').replace(';', '\\;').replace('#', '\\#').replace('\\', '\\\\').replace('\n', '\\n')
                metadata_file.write(f"{key}={escaped_value}\n")
            metadata_file_path = metadata_file.name

        # Comando FFmpeg usando arquivo de metadados
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', metadata_file_path,
            '-map_metadata', '1',  # Usa metadados do segundo input (o arquivo de texto)
            '-c', 'copy',          # Copia streams sem recodificar
            '-y', output_path      # Sobrescreve arquivo de saída
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        # Remove arquivo temporário
        if os.path.exists(metadata_file_path):
            os.unlink(metadata_file_path)
            
        if result.returncode != 0:
            raise Exception(f"Erro FFmpeg ao inserir metadados: {result.stderr}")
            
    except Exception as e:
        raise Exception(f"Erro ao inserir metadados: {e}")
