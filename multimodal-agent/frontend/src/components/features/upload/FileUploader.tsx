import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, Image, Loader2, CheckCircle, XCircle } from "lucide-react";

// Allowed image types only - NO PDFs!
const ACCEPTED_FILE_TYPES = {
    "image/png": [".png"],
    "image/jpeg": [".jpg", ".jpeg"],
    "image/gif": [".gif"],
    "image/webp": [".webp"],
};

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

type UploadStatus = "idle" | "uploading" | "success" | "error";

/**
 * File uploader component with drag-and-drop support.
 * Only accepts image files (PNG, JPG, GIF, WebP).
 */
export function FileUploader() {
    const [status, setStatus] = useState<UploadStatus>("idle");
    const [errorMessage, setErrorMessage] = useState<string>("");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    const onDrop = useCallback(async (acceptedFiles: File[], rejectedFiles: any[]) => {
        // Handle rejected files
        if (rejectedFiles.length > 0) {
            const rejection = rejectedFiles[0];
            const error = rejection.errors[0];

            if (error.code === "file-invalid-type") {
                setErrorMessage(
                    "Invalid file type. Only images are supported (PNG, JPG, GIF, WebP). PDF support coming in Phase 2."
                );
            } else if (error.code === "file-too-large") {
                setErrorMessage("File is too large. Maximum size is 10 MB.");
            } else {
                setErrorMessage(error.message);
            }
            setStatus("error");
            return;
        }

        // Handle accepted file
        if (acceptedFiles.length > 0) {
            const file = acceptedFiles[0];
            setUploadedFile(file);
            setStatus("uploading");
            setErrorMessage("");

            try {
                // TODO: Implement actual file upload to API
                // For now, simulate upload
                await new Promise((resolve) => setTimeout(resolve, 1500));

                // const formData = new FormData();
                // formData.append("file", file);
                // const response = await fetch("/api/v1/files/upload", {
                //   method: "POST",
                //   body: formData,
                //   headers: { Authorization: `Bearer ${token}` },
                // });

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
          transition-colors duration-200
          ${isDragActive && !isDragReject ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20" : ""}
          ${isDragReject ? "border-red-500 bg-red-50 dark:bg-red-900/20" : ""}
          ${status === "success" ? "border-green-500 bg-green-50 dark:bg-green-900/20" : ""}
          ${status === "error" ? "border-red-500 bg-red-50 dark:bg-red-900/20" : ""}
          ${status === "idle" ? "border-slate-300 hover:border-blue-400 hover:bg-slate-50 dark:border-slate-600 dark:hover:border-blue-500 dark:hover:bg-slate-700/50" : ""}
        `}
            >
                <input {...getInputProps()} />

                {status === "idle" && (
                    <div className="space-y-4">
                        <div className="mx-auto w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                            <Upload className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                        </div>
                        <div>
                            <p className="text-lg font-medium">
                                {isDragActive ? "Drop the image here" : "Drag & drop an image"}
                            </p>
                            <p className="text-sm text-slate-500 mt-1">
                                or click to browse (PNG, JPG, GIF, WebP • Max 10 MB)
                            </p>
                        </div>
                    </div>
                )}

                {status === "uploading" && (
                    <div className="space-y-4">
                        <Loader2 className="mx-auto h-12 w-12 animate-spin text-blue-600" />
                        <p className="text-lg font-medium">Uploading {uploadedFile?.name}...</p>
                    </div>
                )}

                {status === "success" && (
                    <div className="space-y-4">
                        <CheckCircle className="mx-auto h-12 w-12 text-green-600" />
                        <div>
                            <p className="text-lg font-medium text-green-700 dark:text-green-400">
                                Upload successful!
                            </p>
                            <p className="text-sm text-slate-500 mt-1">{uploadedFile?.name}</p>
                        </div>
                    </div>
                )}

                {status === "error" && (
                    <div className="space-y-4">
                        <XCircle className="mx-auto h-12 w-12 text-red-600" />
                        <div>
                            <p className="text-lg font-medium text-red-700 dark:text-red-400">
                                Upload failed
                            </p>
                            <p className="text-sm text-red-500 mt-1">{errorMessage}</p>
                        </div>
                    </div>
                )}
            </div>

            {/* Reset button */}
            {(status === "success" || status === "error") && (
                <button
                    onClick={resetUploader}
                    className="w-full rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-50 dark:border-slate-600 dark:hover:bg-slate-700 transition-colors"
                >
                    Upload Another Image
                </button>
            )}

            {/* File type notice */}
            <p className="text-xs text-center text-slate-400">
                📸 Only image files are supported. PDF support coming in Phase 2.
            </p>
        </div>
    );
}
