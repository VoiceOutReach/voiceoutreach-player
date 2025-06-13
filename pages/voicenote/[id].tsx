import { useRouter } from 'next/router';
import Head from 'next/head';
import { useEffect, useState } from 'react';

export default function VoiceNotePage() {
  const router = useRouter();
  const { id } = router.query;
  const [audioSrc, setAudioSrc] = useState<string | null>(null);
  const [name, setName] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      const parts = (id as string).split('_');
      setName(parts[0]);
      setAudioSrc(`/voices/${id}.mp3`);
    }
  }, [id]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
      <Head>
        <title>Voice Message from VoiceOutReach.ai</title>
      </Head>

      <div className="max-w-md w-full bg-white shadow-xl rounded-2xl p-6 text-center">
        <h1 className="text-2xl font-semibold mb-2">🎧 New Voice Message</h1>
        <p className="mb-4 text-gray-600">
          This voice note was sent to you via <strong>VoiceOutReach.ai</strong>
        </p>
        {audioSrc && (
          <audio controls className="w-full mb-4">
            <source src={audioSrc} type="audio/mp3" />
            Your browser does not support the audio element.
          </audio>
        )}
        <a
          href="https://www.linkedin.com/messaging/"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Reply on LinkedIn
        </a>
      </div>
    </div>
  );
}
