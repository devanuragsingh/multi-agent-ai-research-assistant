function UploadProgress({

  progress = 0

}) {

  return (

    <div className="upload-progress">

      <p>

        Uploading...

      </p>

      <progress

        value={progress}

        max="100"

      />

    </div>

  );

}

export default UploadProgress;