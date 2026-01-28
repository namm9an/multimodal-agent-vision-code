import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, Loader2, CheckCircle, XCircle } from "lucide-react";


// Allowed image types only
const ACCEPTED_FILE_TYPES = {
    "image/png": [".png"],
    "image/jpeg": [".jpg", ".jpeg"],
    "image/gif": [".gif"],
    "image/webp": [".webp"],
};

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

type UploadStatus = "idle" | "uploading" | "success" | "error";

/**
 * Dark-themed file uploader with drag-and-drop.
 */
export function FileUploader() {
    const [status, setStatus] = useState<UploadStatus>("idle");
    const [errorMessage, setErrorMessage] = useState<string>("");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    const onDrop = useCallback(async (acceptedFiles: File[], rejectedFiles: any[]) => {
        if (rejectedFiles.length > 0) {
            const rejection = rejectedFiles[0];
            const error = rejection.errors[0];

            if (error.code === "file-invalid-type") {
                setErrorMessage("Only images supported (PNG, JPG, GIF, WebP)");
            } else if (error.code === "file-too-large") {
                setErrorMessage("File too large. Max 10 MB.");
            } else {
                setErrorMessage(error.message);
            }
            setStatus("error");
            return;
        }

        if (acceptedFiles.length > 0) {
            const file = acceptedFiles[0];
            setUploadedFile(file);
            setStatus("uploading");
            setErrorMessage("");

            try {
                // TODO: Implement actual file upload to API
                await new Promise((resolve) => setTimeout(resolve, 1500));
                setStatus("success");
            } catch (error) {
                setStatus("error");
                setErrorMessage("Upload failed. Please try again.");
            }
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
        onDrop,
        accept: ACCEPTED_FILE_TYPES,
        maxSize: MAX_FILE_SIZE,
        maxFiles: 1,
    });

    const resetUploader = () => {
        setStatus("idle");
        setUploadedFile(null);
        setErrorMessage("");
    };

    return (
        <div className="space-y-4">
            {/* Dropzone */}
            <div
                {...getRootProps()}
                className={`
                    border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
                    transition-all duration-200 hover:scale-[1.01] active:scale-[0.99]
                    ${isDragActive && !isDragReject ? "border-indigo-500 bg-indigo-500/10" : ""}
                    ${isDragReject ? "border-red-500 bg-red-500/10" : ""}
                    ${status === "success" ? "border-green-500 bg-green-500/10" : ""}
                    ${status === "error" ? "border-red-500 bg-red-500/10" : ""}
                    ${status === "idle" ? "border-white/20 hover:border-white/40 hover:bg-white/5" : ""}
                `}
            >
                <input {...getInputProps()} />


                {status === "idle" && (
                    <div className="space-y-4">
                        <div className="mx-auto w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center">
                            <Upload className="h-7 w-7 text-white/50" />
                        </div>
                        <div>
                            <p className="text-lg font-medium text-white">
                                {isDragActive ? "Drop the image here" : "Drag & drop an image"}
                            </p>
                            <p className="text-sm text-white/40 mt-1">
                                or click to browse (PNG, JPG, GIF, WebP • Max 10 MB)
                            </p>
                        </div>
                    </div>
                )}

                {status === "uploading" && (
                    <div className="space-y-4">
                        <Loader2 className="mx-auto h-12 w-12 animate-spin text-indigo-400" />
                        <p className="text-lg font-medium text-white">Uploading {uploadedFile?.name}...</p>
                    </div>
                )}

                {status === "success" && (
                    <div className="space-y-4">
                        <CheckCircle className="mx-auto h-12 w-12 text-green-400" />
                        <div>
                            <p className="text-lg font-medium text-green-400">Upload successful!</p>
                            <p className="text-sm text-white/40 mt-1">{uploadedFile?.name}</p>
                        </div>
                    </div>
                )}

                {status === "error" && (
                    <div className="space-y-4">
                        <XCircle className="mx-auto h-12 w-12 text-red-400" />
                        <div>
                            <p className="text-lg font-medium text-red-400">Upload failed</p>
                            <p className="text-sm text-red-300/60 mt-1">{errorMessage}</p>
                        </div>
                    </div>
                )}
            </div>

            {/* Reset button */}
            {(status === "success" || status === "error") && (
                <button
                    onClick={resetUploader}
                    className="w-full rounded-xl border border-white/10 px-4 py-3 text-sm font-medium text-white/70 hover:bg-white/5 hover:scale-[1.01] active:scale-[0.99] transition-all"
                >
                    Upload Another Image
                </button>
            )}
        </div>
    );
}
