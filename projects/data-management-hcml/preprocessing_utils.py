import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime


def clean_filename_column(df, source_col='FileName', new_col='FileNameClean', to_lower=False, to_title=True):
    """
    Membersihkan nama file dari karakter asing, simbol, dan spasi berlebih.
    """
    series = df[source_col].astype(str)

    # Bersihkan karakter asing: kurung, tanda baca, simbol
    series = series.str.replace(r'[\[\]\(\)\{\}_\-]', ' ', regex=True)
    series = series.str.replace(r'[^\w\s]', '', regex=True)
    series = series.str.replace(r'\s+', ' ', regex=True)
    series = series.str.strip()

    # Format huruf
    if to_lower:
        series = series.str.lower()
    elif to_title:
        series = series.str.title()

    df[new_col] = series
    return df

# 1. Normalisasi ekstensi file
def normalize_extensions(df, ext_column='FileExt'):
    """
    Normalisasi ekstensi file: lowercase dan hapus titik.
    """
    df[ext_column] = df[ext_column].astype(str).str.lower().str.replace('.', '', regex=False)
    return df

# 2. Pulihkan ekstensi dari nama file jika kolom kosong
def recover_extensions_from_filename(df, ext_column='FileExt', filename_column='FileName'):
    """
    Jika ekstensi kosong atau unknown, coba pulihkan dari FileName.
    """
    mask = (df[ext_column].isna()) | (df[ext_column].str.lower().isin(['nan', 'none', 'unknown', '']))
    recovered_ext = df.loc[mask, filename_column].str.extract(r'\.([a-zA-Z0-9]+)$')[0]
    recovered_ext = recovered_ext.str.lower().fillna('unknown')
    df.loc[mask, ext_column] = recovered_ext
    print(f"✅ Ekstensi dipulihkan dari FileName: {recovered_ext.notna().sum()} file")
    return df

# 3. Isi missing value default 'unknown'
def handle_missing_extensions(df, ext_column='FileExt'):
    df[ext_column] = df[ext_column].fillna('unknown')
    return df

# 4. Klasifikasi ekstensi → FileType
def classify_extensions(df, ext_column='FileExt', new_column='FileType'):
    """
    Klasifikasikan ekstensi ke dalam jenis file berdasarkan peta.
    """
    extension_map = {
    # Image
    'ai': 'image', 'svg': 'image', 'emf': 'image', 'ico': 'image', 'webp': 'image',
    'tiff': 'image', 'jpg': 'image', 'jpeg': 'image',

    # Font/Web
    'ttf': 'web', 'woff2': 'web', 'otf': 'web', 'eot': 'web',

    # GIS / Mapping
    'mxd': 'gis', 'lyr': 'gis', 'gpx': 'gis', 'gml': 'gis', 'kml': 'gis', 'gpkg': 'gis', 'jgwx': 'gis', 'gmw': 'gis', 'qgz': 'gis',

    # CAD / Engineering
    'dwg': 'cad', 'dxf': 'cad', 'stl': 'cad', 'las': 'cad',

    # Design / Creative
    'psd': 'design', 'indd': 'design', 'cr2': 'design', 'cdr': 'design',

    # Programming / Code
    'bat': 'code', 'htm': 'code', 'bib': 'code', 'lib': 'code', 'cfg': 'code', 'src': 'code', 'yml': 'code',

    # System / OS
    'lock': 'system', 'policy': 'system', 'vm': 'system', 'inf': 'system', 'access': 'system', 'msi': 'system', 'gitignore': 'system', 'checksum': 'system',

    # Package / Install
    'whl': 'package', 'tar': 'package', 'cab': 'package', 'zip': 'archive',

    # Audio / Subtitle
    'sub': 'subtitle', 'srt': 'subtitle',

    # Data / Science / DB
    'pbix': 'data', 'tsv': 'data', 'qmd': 'data',

    # Project / Tools
    'ps': 'project', 'template': 'project', 'tbx': 'project', 'qtr': 'project', 'sdmod': 'project',

    # Tambahan (tandai dulu, bisa dievaluasi lagi)
    'atx': 'gis', 
    'dir': 'gis', 'dlis': 
    'geoscience', 
    'freelist': 'geoscience',
    'bfc': 'geoscience', 
    'certs': 'security', 
    'ja': 'code', 
    'clu': 'code',
    'security': 'security', 
    'net': 'code', 
    'vt': 'project', 
    'gpkg-journal': 'gis',
    '3gp': 'video', 
    'avif': 'image', 
    'jfc': 'code', 
    'properties':'config',
    'tfw':'gis',
    'gsg':'gis',
    'hdr':'gis',
    'segy':'geoscience',
    'eaf':'audio',
    'pfsx':'project',
    'vec':'gis',
    'xlsm':'spreadsheet',
    'jgw':'gis',
    'url':'web', 
    
    'unknown': 'unknown',
    
    'pdf': 'document',
    'docx': 'document',
    'doc': 'document',
    'xlsx': 'spreadsheet',
    'xls': 'spreadsheet',
    'pptx': 'presentation',
    'txt': 'text',
    'md': 'text',
    'csv': 'spreadsheet',
    'ipynb': 'notebook',
    'html': 'web',
    'css': 'web',
    'js': 'web',
    'woff': 'web',
    'mp3': 'audio',
    'wav': 'audio',
    'm4a': 'audio',
    'mp4': 'video',
    'avi': 'video',
    'mov': 'video',
    'png': 'image',
    'bmp': 'image',
    'gif': 'image',
    'tif': 'image',
    'shp': 'gis',
    'shx': 'gis',
    'dbf': 'gis',
    'cpg': 'gis',
    'prj': 'gis',
    'sbx': 'gis',
    'sbn': 'gis',
    'gdbtable': 'gis',
    'gdbtablx': 'gis',
    'gdbindexes': 'gis',
    'imd': 'gis',
    'adf': 'gis',
    'nit': 'gis',
    'spx': 'gis',
    'ovr': 'gis',
    'ini': 'system',
    'dll': 'system',
    'exe': 'system',
    'jar': 'package',
    '7z': 'archive',
    'rar': 'archive',
    'json': 'data',
    'xml': 'data',
    'dat': 'data',
    'prproj': 'project',
    'pf2': 'project'
    }
    
    df[new_column] = df[ext_column].map(extension_map).fillna('other')
    return df

# 5. Analisis: Jumlah dan persentase tiap FileType
def summarize_filetypes(df, filetype_column='FileType'):
    """
    Mengembalikan DataFrame dengan ringkasan jumlah dan persentase file tiap jenis.
    """
    summary = df[filetype_column].value_counts().reset_index()
    summary.columns = ['FileType', 'Count']
    summary['Percentage'] = (summary['Count'] / summary['Count'].sum() * 100).round(2)
    return summary

# 6. Visualisasi Pie Chart FileType
def plot_filetype_distribution(df_summary):
    """
    Pie chart distribusi jenis file.
    """
    colors = plt.cm.tab20.colors
    plt.figure(figsize=(7, 7))
    plt.pie(df_summary['Count'], labels=df_summary['FileType'], autopct='%1.1f%%', colors=colors)
    plt.title('Distribusi Jenis File')
    plt.axis('equal')
    plt.show()

# 7. Tampilkan file yang belum terklasifikasi
def get_other_filetypes(df, type_column='FileType', ext_column='FileExt'):
    """
    Kembalikan daftar ekstensi yang belum terklasifikasi (kategori 'other').
    """
    return df[df[type_column] == 'other'][ext_column].value_counts()

# 8. Refinement interaktif
def refine_filetypes(df, ext_column='FileExt', filetype_column='FileType', filename_column='FileName', top_n=20):
    """
    Memungkinkan pengguna memasukkan kategori baru untuk ekstensi yang belum diklasifikasikan.
    """
    others_df = df[df[filetype_column] == 'other'].copy()
    top_exts = others_df[ext_column].value_counts().head(top_n)

    print("\n🔍 Top 'other' ekstensi yang belum diklasifikasikan:")
    print(top_exts)

    for ext in top_exts.index:
        suggestion = input(f"\nMasukkan kategori untuk ekstensi '.{ext}' (atau tekan Enter untuk lewati): ")
        if suggestion:
            df.loc[df[ext_column] == ext, filetype_column] = suggestion

    updated_others = df[df[filetype_column] == 'other'].shape[0]
    print(f"\n✅ Jumlah file yang masih 'other': {updated_others}")
    return df

def classify_document_age(df, date_col='DateModified', prefix=''):
    """
    Menambahkan kolom tahun, bulan, dan klasifikasi usia dokumen ke dalam DataFrame.

    Parameters:
    - df : pandas.DataFrame
    - date_col : str, nama kolom tanggal yang akan digunakan
    - prefix : str, optional prefix untuk nama kolom hasil

    Returns:
    - df : DataFrame dengan kolom baru:
        [prefix + 'Year', prefix + 'Month', prefix + 'UsiaDokumen']
    """
    # Pastikan kolom bertipe datetime
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)

    # Tambah kolom tahun dan bulan
    df[prefix + 'Year'] = df[date_col].dt.year
    df[prefix + 'Month'] = df[date_col].dt.month

    now = pd.Timestamp(datetime.now())

    # Fungsi klasifikasi usia
    def label_usia_dokumen(date):
        if pd.isna(date):
            return 'tidak diketahui'
        delta = (now - date).days
        if delta <= 365:
            return 'baru'
        elif delta <= 5 * 365:
            return 'menengah'
        else:
            return 'lama'

    df[prefix + 'UsiaDokumen'] = df[date_col].apply(label_usia_dokumen)
    return df

def plot_usia_dokumen(df, usia_col='UsiaDokumen'):
    counts = df[usia_col].value_counts().reindex(['baru', 'menengah', 'lama', 'tidak diketahui'], fill_value=0)
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Distribusi Usia Dokumen')
    plt.xlabel('Kategori Usia')
    plt.ylabel('Jumlah Dokumen')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


# --- ANALISIS UKURAN FILE ---
def add_size_columns(df):
    df['Size_KB'] = pd.to_numeric(df['Size_KB'], errors='coerce').fillna(0)
    df['Size_MB'] = df['Size_KB'] / 1024
    df['SizeCategory'] = df['Size_KB'].apply(classify_size)
    return df

def classify_size(size_kb):
    if size_kb < 100:
        return 'Kecil (<100KB)'
    elif size_kb < 1024:
        return 'Sedang (100KB–1MB)'
    else:
        return 'Besar (>1MB)'

# --- KLASIFIKASI SUMBER FILE ---
def clean_source(df):
    df['Source'] = df['Source'].str.strip().str.lower()
    mapping = {
        'local': 'lokal', 'google drive': 'gdrive', 'unggahan': 'upload',
        'lokal': 'lokal', 'gdrive': 'gdrive', 'email': 'email', 'upload': 'upload',
    }
    df['Source'] = df['Source'].map(mapping).fillna(df['Source'])
    df['Source'] = df['Source'].fillna('unknown')
    df['Source_Class'] = df['Source'].apply(classify_source)
    return df

def classify_source(val):
    if 'gdrive' in val or 'google' in val:
        return 'Cloud'
    elif 'local' in val or 'lokal' in val:
        return 'Offline'
    elif 'email' in val:
        return 'Email'
    else:
        return 'Lainnya'

# --- ANALISIS PATH ---
def standardize_path(df):
    df['Path_modified'] = df['Path'].str.strip().str.replace('\\', '/', regex=False).str.replace('%20', ' ', regex=False)
    return df

def extract_path_levels(df):
    df['Folder_Root'] = df['Path_modified'].apply(lambda x: x.split('/')[0] if pd.notnull(x) else 'unknown')
    df['Subfolder_L2'] = df['Path_modified'].apply(lambda x: x.split('/')[1] if pd.notnull(x) and len(x.split('/')) > 1 else 'unknown')
    df['Subfolder_L3'] = df['Path_modified'].apply(lambda x: x.split('/')[2] if pd.notnull(x) and len(x.split('/')) > 2 else 'unknown')
    df['Subfolder_L4'] = df['Path_modified'].apply(lambda x: x.split('/')[3] if pd.notnull(x) and len(x.split('/')) > 3 else 'unknown')
    df['Subfolder_L5'] = df['Path_modified'].apply(lambda x: x.split('/')[4] if pd.notnull(x) and len(x.split('/')) > 4 else 'unknown')
    df['Subfolder_L6'] = df['Path_modified'].apply(lambda x: x.split('/')[5] if pd.notnull(x) and len(x.split('/')) > 5 else 'unknown')
    df['Filename'] = df['Path_modified'].apply(lambda x: x.split('/')[-1] if pd.notnull(x) else '')
    return df

def classify_path(path):
    path = path.lower()
    if 'projecta' in path:
        return 'Project A'
    elif 'backup' in path:
        return 'Backup'
    elif 'unduh' in path or 'download' in path:
        return 'Downloaded'
    else:
        return 'Lainnya'

def add_path_classification(df):
    df['Path_Class'] = df['Path_modified'].apply(classify_path)
    df['Path_Anomali'] = df['Path_modified'].apply(
        lambda x: 'Yes' if x.lower().startswith(('c:/users', '/users')) else 'No'
    )
    df['Path_Uniform'] = df[['Folder_Root', 'Subfolder_L2', 'Subfolder_L3', 'Subfolder_L4', 'Subfolder_L5']].agg('/'.join, axis=1)
    return df

def check_unique_column(df, col_name):
    return df[col_name].is_unique
