import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import type { Request, Response } from 'express';

@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const res = ctx.getResponse<Response>();
    const req = ctx.getRequest<Request>();

    const isHttp = exception instanceof HttpException;
    const status = isHttp
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    const base = {
      timestamp: new Date().toISOString(),
      path: req.url,
      status,
    };

    if (isHttp) {
      const raw = exception.getResponse() as HttpException;
      const body = typeof raw === 'string' ? { message: raw } : (raw ?? {});

      const message = Array.isArray(body.message)
        ? body.message.join('; ')
        : (body.message ?? exception.message);

      return res.status(status).json({
        ...base,
        ...body,
        message,
      });
    }

    if (exception instanceof Error) {
      return res.status(status).json({
        ...base,
        error: exception.name || 'InternalServerError',
        message: exception.message || 'Internal server error',
        ...(process.env.NODE_ENV !== 'production' && {
          stack: exception.stack,
        }),
      });
    }

    return res.status(status).json({
      ...base,
      error: 'InternalServerError',
      message: 'Internal server error',
    });
  }
}
